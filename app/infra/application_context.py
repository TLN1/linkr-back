from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Annotated, Any, Callable

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.core.application_context import IApplicationContext
from app.core.models import Account, TokenData
from app.core.repository.account_repository import IAccountRepository
from app.infra.auth_utils import oauth2_scheme


@dataclass
class InMemoryApplicationContext(IApplicationContext):
    account_repository: IAccountRepository
    hash_verifier: Callable[[str, str], bool]
    active_accounts: dict[str, str] = field(default_factory=dict)

    def authenticate_user(self, username: str, password: str) -> Account:
        account = self.account_repository.get_account(username)

        if account is not None and self.hash_verifier(password, account.password):
            return account

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    def create_access_token(self, account: Account) -> str:
        token = "token_" + account.username
        self.active_accounts[token] = account.username
        return token

    def get_current_user(self, token: Any) -> Account:
        unauthorized_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )

        if token is None or token not in self.active_accounts:
            raise unauthorized_exception

        account = self.account_repository.get_account(self.active_accounts[token])

        if account is None:
            raise unauthorized_exception

        return account

    def logout_user(self, token: str) -> None:
        del self.active_accounts[token]


# TODO: move secret key somewhere safe?
@dataclass
class InMemoryOauthApplicationContext(IApplicationContext):
    account_repository: IAccountRepository
    hash_verifier: Callable[[str, str], bool]
    secret_key: str = "1ac93dcf0709667ebc635b3547a76af1f824ca43646241cfb4640cf21b940112"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    def authenticate_user(self, username: str, password: str) -> Account:
        authentication_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user = self.account_repository.get_account(username)

        if user is None:
            raise authentication_exception
        if not self.hash_verifier(password, user.password):
            raise authentication_exception

        return user

    def create_access_token(self, account: Account) -> str:
        data: dict[str, Any] = {"sub": account.username}
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return str(encoded_jwt)

    def get_current_user(
        self, token: Any = Annotated[str, Depends(oauth2_scheme)]
    ) -> Account:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        if token_data.username is None:
            raise credentials_exception

        user = self.account_repository.get_account(token_data.username)
        if user is None:
            raise credentials_exception
        return user

    def logout_user(self, token: str) -> None:
        return

"""
user_service.py: File, containing user service.
"""


from typing import ClassVar, Optional
from datetime import datetime
from dataclasses import dataclass
from collections.abc import Iterable
from django.shortcuts import get_object_or_404
from jauth.models import User


@dataclass
class UserDTO:
    """
    UserDTO: User data transfer object.
    """

    pk: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_joined: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: Optional[bool] = None
    is_staff: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserService:
    """
    UserService: User service class. It handles CRUD operations with User resource.
    """

    model_class: ClassVar[type[User]] = User

    def _make_user_dto(self, user: User) -> UserDTO:
        """
        _make_user_dto: Make user DTO from User instance.

        Args:
            user (User): User instance.

        Returns:
            UserDTO: UserDTO.
        """

        return UserDTO(
            pk=user.pk,
            username=user.username,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            date_joined=user.date_joined,
            last_updated=user.last_updated,
            last_login=user.last_login,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_verified=user.is_verified,
        )

    def _prepare_user(self, dto: UserDTO) -> dict[str, str]:
        """
        _prepare_user: Make user dict from UserDTO.

        Args:
            dto (UserDTO): User DTO.

        Returns:
            dict[str, str]: User dict object.
        """

        user: dict[str, Optional[str]] = {
            'username': dto.username,
            'email': dto.email,
            'password': dto.password,
            'first_name': dto.first_name,
            'last_name': dto.last_name,
        }

        return {field: value for field, value in user.items() if value}

    def create(self, dto: UserDTO) -> UserDTO:
        """
        create: Create User instance.

        Args:
            dto (UserDTO): UserDTO.

        Returns:
            UserDTO: UserDTO.
        """

        user_data: dict[str, str] = self._prepare_user(dto)
        user: User = self.model_class.objects.create(**user_data)
        user.set_password(user.password)

        return self._make_user_dto(user)

    def get_all(self) -> Iterable[UserDTO]:
        """
        get_all: Return iterable with UserDTO.

        Returns:
            Iterable[UserDTO]: Map object with UserDTO.
        """

        users: Iterable[User] = self.model_class.objects.all()

        return map(self._make_user_dto, users)

    def get_by_pk(self, pk: int) -> UserDTO:
        """
        get_by_pk: Return UserDTO by pk.

        Args:
            pk (int): pk of the User instance.

        Returns:
            UserDTO: UserDTO.
        """

        user: User = get_object_or_404(self.model_class, pk=pk)

        return self._make_user_dto(user)

    def update(self, pk: int, dto: UserDTO) -> UserDTO:
        """
        update: Update User instance.

        Args:
            pk (int): pk of the User instance.
            dto (UserDTO): UserDTO.

        Returns:
            UserDTO: UserDTO.
        """

        user_data: dict[str, str] = self._prepare_user(dto)
        self.model_class.objects.filter(pk=pk).update(**user_data)
        user: User = get_object_or_404(self.model_class, pk=pk)

        if 'password' in user_data:
            user.set_password(user.password)

        return self._make_user_dto(user)

    def destroy(self, pk: int) -> None:
        """
        destroy: Make is_active field False of the User instance.

        Args:
            pk (int): pk of the User instance.
        """

        user: User = get_object_or_404(self.model_class, pk=pk)
        user.set_is_active(False)

    def make_user_unferified(self, pk: int) -> None:
        """
        make_user_unferified: Make is_verified field False of the User instance.

        Args:
            pk (int): pk of the User instance.
        """

        user: User = get_object_or_404(self.model_class, pk=pk)
        user.set_is_verified(False)

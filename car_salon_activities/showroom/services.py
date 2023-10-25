"""
sevices.py: File, containing services for a showroom application.
"""


from showroom.models import ShowroomModel


class ShowroomService:
    """
    ShowroomService: Contains business logic for Showroom resourse.
    """

    def delete_showroom(self, showroom: ShowroomModel) -> None:
        """
        delete_showroom: Sets showroom's is_active field to False.

        Args:
            showroom (ShowroomModel): Showroom instance.
        """

        showroom.is_active = False
        showroom.save()

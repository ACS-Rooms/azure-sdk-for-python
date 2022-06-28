# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from datetime import datetime
from typing import TYPE_CHECKING
import uuid
from azure.core.tracing.decorator import distributed_trace
from azure.communication.rooms._models import RoomModel, RoomParticipant

from ._generated._client import AzureCommunicationRoomsService
from ._generated.models import (
    CreateRoomRequest,
    UpdateRoomRequest,
    RemoveParticipantsRequest,
    AddParticipantsRequest,
    UpdateParticipantsRequest,
    CommunicationIdentifierModel
)

from ._shared.utils import parse_connection_str, get_authentication_policy
from ._version import SDK_MONIKER
from ._api_versions import DEFAULT_VERSION

if TYPE_CHECKING:
    from typing import Any

class RoomsClient(object):
    """A client to interact with the AzureCommunicationService Rooms gateway.

    This client provides operations to manage rooms.

    :param str endpoint:
        The endpoint url for Azure Communication Service resource.
    :param TokenCredential credential:
        The TokenCredential we use to authenticate against the service.
    """
    def __init__(
            self, endpoint, # type: str
            credential, # type: TokenCredential
            **kwargs # type: Any
    ):
        # type: (...) -> None
        try:
            if not endpoint.lower().startswith('http'):
                endpoint = "https://" + endpoint
        except AttributeError:
            raise ValueError("Account URL must be a string.")

        if not credential:
            raise ValueError(
                "invalid credential from connection string.")

        self._endpoint = endpoint
        self._api_version = kwargs.pop("api_version", DEFAULT_VERSION)
        self._authentication_policy = get_authentication_policy(endpoint, credential)
        self._rooms_service_client = AzureCommunicationRoomsService(
            self._endpoint,
            api_version = self._api_version,
            authentication_policy=self._authentication_policy,
            sdk_moniker=SDK_MONIKER,
            **kwargs)

    @classmethod
    def from_connection_string(cls, conn_str,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> RoomsClient
        """Create RoomsClient from a Connection String.

        :param str conn_str:
            A connection string to an Azure Communication Service resource.
        :returns: Instance of RoomsClient.
        :rtype: ~azure.communication.RoomsClient

        .. admonition:: Example:

            .. literalinclude:: ../samples/Rooms_sample.py
                :start-after: [START auth_from_connection_string]
                :end-before: [END auth_from_connection_string]
                :language: python
                :dedent: 8
                :caption: Creating the RoomsClient from a connection string.
        """
        endpoint, access_key = parse_connection_str(conn_str)

        return cls(endpoint, access_key, **kwargs)

    @distributed_trace
    def create_room(
        self,
        valid_from=None, # type: Optional[datetime]
        valid_until=None, # type: Optional[datetime]
        roomOpen=None, # type Optional[bool]
        participants=None, # type: Optional[List[RoomParticipant]]
        **kwargs
    ):
        # type: (...) -> RoomModel
        """Create a new room.

        :param valid_from: The timestamp from when the room is open for joining. The timestamp is in
         RFC3339 format: ``yyyy-MM-ddTHH:mm:ssZ``.
        :type valid_from: ~datetime
        :param valid_until: The timestamp from when the room can no longer be joined. The timestamp
         is in RFC3339 format: ``yyyy-MM-ddTHH:mm:ssZ``.
        :type valid_until: ~datetime
        :keyword participants: (Optional) Collection of identities invited to the room.
        :paramtype participants: (Optional)list[RoomParticipant]
        :returns: Created room.
        :rtype: ~azure.communication.rooms.RoomModel
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        create_room_request = CreateRoomRequest(
            valid_from=valid_from,
            valid_until=valid_until,
            room_open=roomOpen,
            participants=participants
        )

        repeatability_request_id = uuid.uuid1()
        repeatability_first_sent = datetime.utcnow()

        create_room_response = self._rooms_service_client.rooms.create_room(
            create_room_request=create_room_request,
            repeatability_request_id=repeatability_request_id,
            repeatability_first_sent=repeatability_first_sent,
            **kwargs)
        return RoomModel.from_room_response(create_room_response)

    @distributed_trace
    def delete_room(
        self,
        room_id, # type: str
        **kwargs
    ):
        # type: (...) -> None
        """Delete room.

        :param room_id: Required. Id of room to be deleted
        :type room_id: str
        :returns: None.
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError

        """
        self._rooms_service_client.rooms.delete_room(room_id=room_id, **kwargs)

    @distributed_trace
    def update_room(
        self,
        room_id,
        valid_from=None, # type: Optional[datetime]
        valid_until=None, # type: Optional[datetime]
        room_open=None, # type: Optional[bool]
        participants=None, #type: Optional[List[RoomParticipant]]
        **kwargs
    ):
        # type: (...) -> RoomModel
        """Update a valid room's attributes

        :param room_id: Required. Id of room to be updated
        :type room_id: str
        :param valid_from: The timestamp from when the room is open for joining. The timestamp is in
         RFC3339 format: ``yyyy-MM-ddTHH:mm:ssZ``.
        :type valid_from: ~datetime
        :param valid_until: The timestamp from when the room can no longer be joined. The timestamp
         is in RFC3339 format: ``yyyy-MM-ddTHH:mm:ssZ``.
        :type valid_until: ~datetime
        :returns: Updated room.
        :rtype: ~azure.communication.rooms.RoomModel
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError

        """
        update_room_request = UpdateRoomRequest(
            valid_from=valid_from,
            valid_until=valid_until,
            room_open=room_open,
            participants=participants,
        )
        update_room_response = self._rooms_service_client.rooms.update_room(
            room_id=room_id, patch_room_request=update_room_request, **kwargs)
        return RoomModel.from_room_response(update_room_response)

    @distributed_trace
    def get_room(
        self,
        room_id, # type: str
        **kwargs
    ):
        # type: (...) -> RoomModel
        """Get a valid room

        :param room_id: Required. Id of room to be fetched
        :type room_id: str
        :returns: Room with current attributes.
        :rtype: ~azure.communication.rooms.RoomModel
        :raises: ~azure.core.exceptions.HttpResponseError

        """
        get_room_response = self._rooms_service_client.rooms.get_room(room_id=room_id, **kwargs)
        return RoomModel.from_room_response(get_room_response)

    @distributed_trace
    def add_participants(
        self,
        room_id, # type: str
        participants, # type: List[RoomParticipant]
        **kwargs
    ):
        # type: (...) -> RoomModel
        """Add participants to a room
        :param room_id: Required. Id of room to be updated
        :type room_id: str
        :param participants: Required. Collection of identities invited to the room.
        :paramtype participants: dict[str, any]
        :returns: Updated room.
        :rtype: ~azure.communication.rooms.RoomModel
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        add_participants_request = AddParticipantsRequest(
            participants=participants
        )
        add_participants_response = self._rooms_service_client.rooms.add_participants(
            room_id=room_id, add_participants_request=add_participants_request, **kwargs)
        return RoomModel.from_room_response(add_participants_response)

    @distributed_trace
    def update_participants(
        self,
        room_id, # type: str
        participants, # type: List[RoomParticipant]
        **kwargs
    ):
        # type: (...) -> RoomModel
        """Update participants to a room
        :param room_id: Required. Id of room to be updated
        :type room_id: str
        :param participants: Required. Collection of identities invited to the room.
        :paramtype participants: dict[str, any]
        :returns: Updated room.
        :rtype: ~azure.communication.rooms.RoomModel
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        update_participants_request = UpdateParticipantsRequest(
            participants=participants
        )
        update_participants_response = self._rooms_service_client.rooms.update_participants(
            room_id=room_id, update_participants_request=update_participants_request, **kwargs)
        return RoomModel.from_room_response(update_participants_response)

    @distributed_trace
    def remove_participants(
        self,
        room_id, # type: str
        communication_identifiers, # type: List[CommunicationIdentifierModel]
        **kwargs
    ):
        # type: (...) -> RoomModel
        """Remove participants from a room
        :param room_id: Required. Id of room to be updated
        :type room_id: str
        :param participants: Required. Collection of identities invited to the room.
        :paramtype participants: dict[str, any]
        :returns: Updated room.
        :rtype: ~azure.communication.rooms.RoomModel
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        participants = [RoomParticipant(communication_identifier=id) for id in communication_identifiers]
        remove_participants_request = RemoveParticipantsRequest(
            participants=participants
        )
        remove_participants_response = self._rooms_service_client.rooms.remove_participants(
            room_id=room_id, remove_participants_request=remove_participants_request, **kwargs)
        return RoomModel.from_room_response(remove_participants_response)

    @distributed_trace
    def remove_all_participants(
        self,
        room_id, # type: str
        **kwargs
    ):
        # type: (...) -> RoomModel
        """Remove all participants from a room
        :param room_id: Required. Id of room to be updated
        :type room_id: str
        :returns: Updated room.
        :rtype: ~azure.communication.rooms.RoomModel
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        update_room_request = UpdateRoomRequest(
            participants=[]
        )
        update_room_response = self._rooms_service_client.rooms.update_room(
            room_id=room_id, patch_room_request=update_room_request, **kwargs)
        return RoomModel.from_room_response(update_room_response)

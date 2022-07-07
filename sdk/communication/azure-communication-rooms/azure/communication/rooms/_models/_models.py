# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------
import msrest.serialization
from typing import Optional

from .._generated.models import (
    RoomModel,
    RoomParticipant,
    CommunicationIdentifierModel,
)
from .._generated import _serialization

class RoomModel(_serialization.Model):
    """The response object from rooms service.

    :ivar id: Unique identifier of a room. This id is server generated.
    :vartype id: str
    :ivar created_date_time: The timestamp when the room was created at the server. The timestamp
     is in RFC3339 format: ``yyyy-MM-ddTHH:mm:ssZ``.
    :vartype created_date_time: ~datetime
    :ivar valid_from: The timestamp from when the room is open for joining. The timestamp is in
     RFC3339 format: ``yyyy-MM-ddTHH:mm:ssZ``.
    :vartype valid_from: ~datetime
    :ivar valid_until: The timestamp from when the room can no longer be joined. The timestamp is
     in RFC3339 format: ``yyyy-MM-ddTHH:mm:ssZ``.
    :vartype valid_until: ~datetime
    :ivar participants: Collection of identities invited to the room.
    :vartype participants: dict[str, any]
    """

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'created_date_time': {'key': 'createdDateTime', 'type': 'iso-8601'},
        'valid_from': {'key': 'validFrom', 'type': 'iso-8601'},
        'valid_until': {'key': 'validUntil', 'type': 'iso-8601'},
        'participants': {'key': 'participants', 'type': '{object}'},
    }

    def __init__(
        self,
        *,
        id=None, # type: Optional[str] pylint: disable=redefined-builtin
        created_date_time=None, # type: Optional[datetime]
        valid_from=None, # type: Optional[datetime]
        valid_until=None, # type: Optional[datetime]
        participants=None, # type: Optional[List[RoomParticipant]]
        **kwargs
    ):
        """
        :keyword id: Unique identifier of a room. This id is server generated.
        :paramtype id: str
        :keyword created_date_time: The timestamp when the room was created at the server. The
         timestamp is in RFC3339 format: ``yyyy-MM-ddTHH:mm:ssZ``.
        :paramtype created_date_time: ~datetime
        :keyword valid_from: The timestamp from when the room is open for joining. The timestamp is in
         RFC3339 format: ``yyyy-MM-ddTHH:mm:ssZ``.
        :paramtype valid_from: ~datetime
        :keyword valid_until: The timestamp from when the room can no longer be joined. The timestamp
         is in RFC3339 format: ``yyyy-MM-ddTHH:mm:ssZ``.
        :paramtype valid_until: ~datetime
        :keyword participants: Collection of identities invited to the room.
        :paramtype participants: dict[str, any]
        """
        super(RoomModel, self).__init__(**kwargs)
        self.id = id
        self.created_date_time = created_date_time
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.participants = participants

    @classmethod
    def from_room_response(cls, get_room_response,  # type: RoomModel
            **kwargs  # type: Any
    ):
        # type: (...) -> CommunicationRoom
        """Create CommunicationRoom from a RoomModel.
        :param RoomModel get_room_response:
            Response from get_room API.
        :returns: Instance of CommunicationRoom.
        :rtype: ~azure.communication.CommunicationRoom
        """
        if get_room_response.participants is None:
            participants = None
        else:
            participants = [RoomParticipant(identifier=identifier, role_name=participant.role) for identifier, participant in get_room_response.participants.items()]

        return cls(
        id=get_room_response.id,
        created_date_time=get_room_response.created_date_time,
        valid_from=get_room_response.valid_from,
        valid_until=get_room_response.valid_until,
        participants=participants,
        **kwargs
        )

class RoomParticipant(_serialization.Model):
    """A participant of the room.

    All required parameters must be populated in order to send to Azure.

    :ivar communication_identifier: Identifies a participant in Azure Communication services. A
     participant is, for example, an Azure communication user. This model must be interpreted as a
     union: Apart from rawId, at most one further property may be set. Required.
    :vartype communication_identifier:
     ~azure.communication.rooms.models.CommunicationIdentifierModel
    :ivar role: Role Name.
    :vartype role: str
    """

    _validation = {
        "communication_identifier": {"required": True},
    }

    _attribute_map = {
        "communication_identifier": {"key": "communicationIdentifier", "type": "CommunicationIdentifierModel"},
        "role": {"key": "role", "type": "str"},
    }

    def __init__(
        self,
        *,
        communication_identifier: CommunicationIdentifierModel,
        role: Optional[str] = None,
        **kwargs
    ):
        """
        :keyword identifier: Participant MRI
        :paramtype identifier: str
        """
        super(RoomParticipant, self).__init__(**kwargs)
        self.communication_identifier = communication_identifier
        self.role = role

    def to_room_participant(self):
        return RoomParticipant(
            communication_identifier=self.communication_identifier,
            role=self.role_name
        )

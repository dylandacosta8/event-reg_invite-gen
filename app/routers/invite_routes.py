from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.invite_service import InviteService
from app.schemas.invite_schemas import InviteCreate, InviteUpdate, InviteResponse, InviteListResponse
from app.dependencies import get_db, get_current_user
from app.models.user_model import User

router = APIRouter()


@router.post("/invites/", response_model=InviteResponse, status_code=201, name="create_invite", tags=["Invitations"])
async def create_invite(
    invite_data: InviteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new invitation linked to the current user.
    """
    new_invite = await InviteService.create_invitation(
        db=db,
        user_id=current_user.id,
        invitee_email=invite_data.invitee_email,
        nickname=invite_data.nickname
    )
    if not new_invite:
        raise HTTPException(status_code=400, detail="Error creating invitation.")
    return new_invite


@router.put("/invites/{invite_id}", response_model=InviteResponse, name="update_invite", tags=["Invitations"])
async def update_invite(
    invite_id: int,
    invite_data: InviteUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an invitation by ID.
    """
    updated_invite = await InviteService.update_invite(
        db=db,
        invite_id=invite_id,
        update_data=invite_data.dict(exclude_unset=True)
    )
    if not updated_invite:
        raise HTTPException(status_code=404, detail="Invitation not found.")
    return updated_invite


@router.get("/invites/{invite_code}", response_model=InviteResponse, name="get_invite_by_code", tags=["Invitations"])
async def get_invite_by_code(
    invite_code: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve an invitation by its invite code.
    """
    invite = await InviteService.get_invite_by_code(db=db, invite_code=invite_code)
    if not invite:
        raise HTTPException(status_code=404, detail="Invitation not found.")
    return invite


@router.get("/invites/", response_model=InviteListResponse, name="list_invites", tags=["Invitations"])
async def list_invites(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all invitations created by the current user.
    """
    invites, total = await InviteService.list_user_invites(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return InviteListResponse(items=invites, total=total, page=skip // limit + 1, size=limit)


@router.get("/invites/validate/{invite_code}", response_model=bool, name="validate_invite_code", tags=["Invitations"])
async def validate_invite_code(
    invite_code: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Validate an invitation code.
    """
    is_valid = await InviteService.validate_invite_code(db=db, invite_code=invite_code)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired invitation code.")
    return True

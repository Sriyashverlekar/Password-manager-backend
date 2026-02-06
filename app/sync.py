from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Device
from app.schemas import DeviceCreate, DeviceResponse
from app.auth import get_current_user

# Sets up a group of routes starting with "/devices" to keep the code organized.
router = APIRouter(prefix="/devices", tags=["Devices"])


# Creates a new device record when a user sends a POST request.
@router.post("/register", response_model=DeviceResponse)
def register_device(
    request: DeviceCreate,                                  # Takes in the device name from the user.
    db: Session = Depends(get_db),                  # Connects to the database.
    current_user: dict = Depends(get_current_user)              # Checks who is logged in so the device is linked to the right person.
):
    # Prepares a new device object using the name provided and the logged-in user's ID.
    device = Device(
        user_id=current_user["user_id"], 
        device_name=request.device_name
    )
    
    # Saves the new device into the database and confirms the change.
    db.add(device)
    db.commit()
    
    # Updates the 'device' variable with information the database created, like its new ID number.
    db.refresh(device)
    return device


# Gets a list of all devices for the person currently logged in.
@router.get("/", response_model=list[DeviceResponse])
def list_devices(
    # Connects to the database to look up records.
    db: Session = Depends(get_db),                
    current_user: dict = Depends(get_current_user)   # Identifies the user to make sure they only see their own data.
):
    # Searches the database for all devices where the owner matches the current user.
    return (
        db.query(Device)
        .filter(Device.user_id == current_user["user_id"])
        .all()
    )

"""Helpers for switch_manager integration."""
import json, pathlib, os, shutil
from homeassistant.util.yaml.loader import _find_files, load_yaml
from .const import LOGGER, DOMAIN, BLUEPRINTS_FOLDER
from homeassistant.exceptions import HomeAssistantError

COMPONENT_PATH = os.path.dirname(os.path.realpath(__file__))

async def load_manifest():
    return json.load(
        open( os.path.join( COMPONENT_PATH, 'manifest.json') )
    )

async def deploy_blueprints( hass ):
    dest_folder = pathlib.Path(hass.config.path(BLUEPRINTS_FOLDER, DOMAIN))
    if not os.path.exists( dest_folder ):
        os.makedirs( dest_folder )
    
    component_blueprints_path = os.path.join( COMPONENT_PATH, 'blueprints' )
    files = os.listdir(component_blueprints_path)
    for file in files:
        shutil.copy( 
            os.path.join( component_blueprints_path, file ),
            dest_folder
        )
    

def _load_blueprints( hass ):
    folder = pathlib.Path(hass.config.path(BLUEPRINTS_FOLDER, DOMAIN))
    results = [];
    for f in _find_files(folder, "*.yaml"):
        try:
            data = load_yaml(f)
        except HomeAssistantError as ex:
            LOGGER.error(str(ex))
            continue
        results.append({
            'id': os.path.splitext(os.path.basename(f))[0],
            'has_image': os.path.exists(
                os.path.join(folder, os.path.splitext(os.path.basename(f))[0] + '.png')
            ),
            'data': data        
        })
    return results
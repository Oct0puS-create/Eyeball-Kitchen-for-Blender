import bpy
from pathlib import Path

def get_addon_directory():
    """Get the add-on's root directory"""
    return Path(__file__).parent

def load_prefab_mesh(prefab_name, collection_name):
    """Load a prefab mesh and its materials from a separate .blend file"""
    addon_dir = get_addon_directory()
    blend_path = addon_dir / "assets" / prefab_name / f"prefabs_{prefab_name}.blend"
    
    if not blend_path.exists():
        raise FileNotFoundError(f"Blend file not found: {blend_path}")
    
    # Load the specific collection
    with bpy.data.libraries.load(str(blend_path)) as (data_from, data_to):
        if collection_name not in data_from.collections:
            raise ValueError(f"Collection '{collection_name}' not found in prefabs_{prefab_name}.blend")
        
        data_to.collections = [collection_name]
        # Also load all materials used by objects in this collection
        data_to.materials = data_from.materials[:]
    
    # Link the collection to the scene
    loaded_collection = None
    for collection in data_to.collections:
        bpy.context.scene.collection.children.link(collection)
        loaded_collection = collection
    
    return loaded_collection


def create_prefab_instance(prefab_name, collection_name, context):
    """Create a new instance of a prefab collection in the scene"""
    collection = load_prefab_mesh(prefab_name, collection_name)
    
    # Select all objects in the loaded collection
    for obj in collection.all_objects:
        obj.select_set(True)
        context.view_layer.objects.active = obj
    
    return collection
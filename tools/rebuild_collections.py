"""Helper script for rebuilding the collection models from schemas.

This expects the schema of https://github.com/leonhard-s/ps2-api-docs,
specifically the files in the `components/schemas` directory.
"""

import argparse
import os
import subprocess

_BASE_CLASS = 'auraxium.models.base.RESTPayload'
_EXTRA_FIELDS = ('x-cast-to', 'x-reference-to')
_REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
_TEMPLATES_DIR = os.path.join(_REPO_ROOT, 'templates')
_COLLECTIONS = (
    'ability',
    'ability_type',
    'achievement',
    'armor_facing',
    'armor_info',
    'character',
    'character_name',
    'characters_achievement',
    'characters_currency',
    'characters_directive',
    'characters_directive_objective',
    'characters_directive_tier',
    'characters_directive_tree',
    'characters_event',
    'characters_event_grouped',
    'characters_friend',
    'characters_item',
    'characters_leaderboard',
    'characters_online_status',
    'characters_skill',
    'characters_stat',
    'characters_stat_by_faction',
    'characters_stat_history',
    'characters_weapon_stat',
    'characters_weapon_stat_by_faction',
    'characters_world',
    'currency',
    'directive',
    'directive_tier',
    'directive_tree',
    'directive_tree_category',
    'effect',
    'effect_type',
    'empire_scores',
    'event',
    'experience',
    'experience_award_type',
    'experience_rank',
    'facility_link',
    'facility_type',
    'faction',
    'fire_group',
    'fire_group_to_fire_mode',
    'fire_mode',
    'fire_mode_2',
    'fire_mode_to_projectile',
    'fire_mode_type',
    'fish',
    'image',
    'image_set',
    'image_set_default',
    'item',
    'item_attachment',
    'item_category',
    'item_profile',
    'item_to_weapon',
    'item_type',
    'leaderboard',
    'loadout',
    'map',
    'map_hex',
    'map_region',
    'marketing_bundle',
    'marketing_bundle_item',
    'marketing_bundle_with_1_item',
    'metagame_event',
    'metagame_event_state',
    'objective',
    'objective_set_to_objective',
    'objective_type',
    'outfit',
    'outfit_member',
    'outfit_member_extended',
    'outfit_rank',
    'player_state',
    'player_state_group',
    'player_state_group_2',
    'profile',
    'profile_2',
    'profile_armor_map',
    'profile_resist_map',
    'projectile',
    'projectile_flight_type',
    'region',
    'resist_info',
    'resist_type',
    'resource_type',
    'reward',
    'reward_group_to_reward',
    'reward_set_to_reward_group',
    'reward_type',
    'single_character_by_id',
    'skill',
    'skill_category',
    'skill_line',
    'skill_set',
    'target_type',
    'title',
    'vehicle',
    'vehicle_attachment',
    'vehicle_faction',
    'vehicle_skill_set',
    'weapon',
    'weapon_ammo_slot',
    'weapon_datasheet',
    'weapon_to_attachment',
    'weapon_to_fire_group',
    'world',
    'world_event',
    'world_stat_history',
    'zone',
    'zone_effect',
    'zone_effect_type',
)


def _snake_case_to_pascal_case(string: str) -> str:
    """Convert a snake_case string to PascalCase.
    
    Args:
        string: The snake_case string to convert.
        
    Returns:
        The converted PascalCase string.
    """
    return ''.join(s.capitalize() for s in string.split('_'))


def _codegen_command(collection: str, schemas_dir: str) -> list[str]:
    """Assemble the datamodel-codegen command for a given collection.
    
    Args:
        collection: The name of the collection (snake_case).
        schemas_dir: The directory where the schema files are located.
    
    Returns:
        A list of command line arguments.
    """
    input_ = os.path.join(schemas_dir, f'{collection}.yaml')
    output = os.path.join(
        _REPO_ROOT, 'auraxium', 'collections', f'{collection}.py')
    class_name = _snake_case_to_pascal_case(collection)
    return [
        'datamodel-codegen',
        '--encoding=utf-8',
        # Input file and type
        f'--input={input_}',
        '--input-file-type=jsonschema',
        # Output file and templates
        f'--output={output}',
        f'--custom-template-dir={_TEMPLATES_DIR}',
        '--output-model-type=pydantic_v2.BaseModel',
        f'--base-class={_BASE_CLASS}',
        f'--class-name={class_name}',
        # Compatibility and formatting
        '--target-python-version=3.10',
        '--disable-future-imports',
        '--reuse-model',
        '--use-union-operator',
        '--use-schema-description',
        '--use-field-description',
        '--field-extra-keys', *_EXTRA_FIELDS,
    ]


def main(schemas_dir: str, incremental: bool) -> None:
    """Rebuild all collection models from their JSON schema definitions.
    
    Args:
        schemas_dir: The directory where the schema files are located.
    """
    print(f'Rebuilding collections from schemas in: {schemas_dir}')
    for collection_name in _COLLECTIONS:
        if not os.path.exists(os.path.join(schemas_dir, f'{collection_name}.yaml')):
            print(f'  Skipping {collection_name}: schema file not found.')
            continue
        if incremental and os.path.exists(os.path.join(
            _REPO_ROOT, 'auraxium', 'collections', f'{collection_name}.py')):
            print(f'  Skipping {collection_name}: already exists.')
            continue
        print(f'Rebuilding {collection_name}...')
        command = _codegen_command(collection_name, schemas_dir)
        subprocess.run(command, check=True)
    print('Rebuilding complete.')


if __name__ == '__main__':
    _parser = argparse.ArgumentParser()
    _parser.add_argument('api_docs_root',
                         help='Path to the root of a ps2-api-docs repository.')
    _parser.add_argument('--incremental', action='store_true',
                         help='Skip collections for existing files.')
    _args = _parser.parse_args()
    _schemas_dir = os.path.join(_args.api_docs_root, 'components', 'schemas')
    main(_schemas_dir, _args.incremental)

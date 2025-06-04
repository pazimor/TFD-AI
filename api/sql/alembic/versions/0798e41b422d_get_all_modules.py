"""get all modules for UI

Revision ID: 0798e41b422d
Revises: a67483573ff3
Create Date: 2025-05-21 20:07:06.186436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '0798e41b422d'
down_revision: Union[str, None] = 'a67483573ff3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS GetAllModules;")
    op.execute(
        """
        CREATE PROCEDURE GetAllModules()
        BEGIN
            CREATE TEMPORARY TABLE tmp_stats
            AS
            SELECT
                ms.module_id,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'level',           ms.level,
                        'module_capacity', ms.module_capacity,
                        'value',           ms.value
                    )
                ) AS stats_json
            FROM (
                SELECT module_id, level, module_capacity, value
                FROM module_stat
                ORDER BY level
            ) AS ms
            GROUP BY ms.module_id;

            SELECT
                m.id,
                m.module_id,
                m.module_name_id,
                m.module_class          AS module_class_id,
                m.module_socket_type    AS module_socket_type_id,
                m.available_module_slot_type AS available_module_slot_type_id,

                m.image_url,
                m.module_type,
                m.module_tier_id,
                m.available_weapon_type,
                m.available_descendant_id,

                tmp.stats_json AS stats
            FROM module AS m
            LEFT JOIN tmp_stats AS tmp ON tmp.module_id = m.module_id
            ORDER BY m.id;
            DROP TEMPORARY TABLE tmp_stats;
        END
        """)
    op.execute("DROP PROCEDURE IF EXISTS GetAllTranslations;")
    op.execute(
        """
        CREATE PROCEDURE GetAllTranslations()
        BEGIN
            SELECT *
            FROM translation_strings
            ORDER BY id;
        END
        """
    )
    op.execute("DROP PROCEDURE IF EXISTS GetAllDescendants;")
    op.execute(
        """
        CREATE PROCEDURE GetAllDescendants()
        BEGIN
            CREATE TEMPORARY TABLE tmp_stat_per_lvl AS
            SELECT
                dsd.descendant_id,
                dsd.level,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'stat_id',    dsd.stat_id,
                        'stat_value', dsd.stat_value
                    )
                ) AS stat_detail_json
            FROM descendant_stat_detail AS dsd
            GROUP BY dsd.descendant_id, dsd.level;

            CREATE TEMPORARY TABLE tmp_stats AS
            SELECT
                ds.descendant_id,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'level',           ds.level,
                        'stat_detail',     t.stat_detail_json
                    )
                    ORDER BY ds.level
                ) AS stats_json
            FROM descendant_stat AS ds
            LEFT JOIN tmp_stat_per_lvl AS t
                   ON t.descendant_id = ds.descendant_id
                  AND t.level         = ds.level
            GROUP BY ds.descendant_id;

            CREATE TEMPORARY TABLE tmp_skills AS
            SELECT
                descendant_id,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'skill_type',      skill_type,
                        'skill_name',      skill_name,
                        'element_type',    element_type,
                        'arche_type',      arche_type,
                        'skill_image_url', skill_image_url,
                        'skill_description', skill_description
                    )
                ) AS skills_json
            FROM descendant_skill
            GROUP BY descendant_id;

            SELECT
                d.id,
                d.descendant_id,
                d.descendant_name,
                d.descendant_group_id,
                d.descendant_image_url,

                COALESCE(ts.stats_json,  JSON_ARRAY()) AS stats,
                COALESCE(sk.skills_json, JSON_ARRAY()) AS skills
            FROM descendant AS d
            LEFT JOIN tmp_stats  AS ts ON ts.descendant_id = d.descendant_id
            LEFT JOIN tmp_skills AS sk ON sk.descendant_id = d.descendant_id
            ORDER BY d.descendant_id;

            DROP TEMPORARY TABLE tmp_stat_per_lvl;
            DROP TEMPORARY TABLE tmp_stats;
            DROP TEMPORARY TABLE tmp_skills;
        END
        """
    )
    op.execute("DROP PROCEDURE IF EXISTS GetAllWeapons;")
    op.execute(
        """
        CREATE PROCEDURE GetAllWeapons()
        BEGIN
            /* 1.  Agrégation des stats par arme ------------------------------ */
            CREATE TEMPORARY TABLE tmp_weapon_stats
            AS
            SELECT
                wbs.weapon_id,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'stat_id',    wbs.stat_id,
                        'stat_value', wbs.stat_value
                    )
                ) AS stats_json
            FROM weapon_base_stat AS wbs
            GROUP BY wbs.weapon_id;

            /* 2.  Sélection finale : méta + stats ---------------------------- */
            SELECT
                w.id,
                w.weapon_id,

                /* IDs bruts (pas de traduction) */
                w.weapon_name_id,
                w.weapon_type        AS weapon_type_id,
                w.weapon_rounds_type AS weapon_rounds_type_id,
                w.weapon_perk_ability_name        AS weapon_perk_name_id,
                w.weapon_perk_ability_description AS weapon_perk_desc_id,

                /* Autres colonnes utiles au front */
                w.image_url,
                w.weapon_tier_id,
                w.available_core_slot,
                w.weapon_perk_ability_image_url,
                w.firearm_atk_type,
                w.firearm_atk_value,

                /* Tableau JSON de stats — vide si aucune entrée dans weapon_base_stat */
                COALESCE(ts.stats_json, JSON_ARRAY()) AS stats
            FROM weapon AS w
            LEFT JOIN tmp_weapon_stats AS ts ON ts.weapon_id = w.weapon_id
            ORDER BY w.weapon_id;

            DROP TEMPORARY TABLE tmp_weapon_stats;
        END;
        """
    )
    op.execute("DROP PROCEDURE IF EXISTS GetWeaponCoreSlots;")
    op.execute(
        """
        CREATE PROCEDURE GetWeaponCoreSlots (IN p_weapon_id INT)
        BEGIN
            SELECT
                w.weapon_id,
                COALESCE(
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'core_slot_id',   cs.core_slot_id,
                            'core_type_id',   cs.available_core_type,
                            'option_type',    cai.option_type,
                            'option_grade',   cai.option_grade,
                            'stat_id',        cai.stat_id,
                            'operator_type',  cai.operator_type,
                            'min_stat_value', cai.min_stat_value,
                            'max_stat_value', cai.max_stat_value,
                            'rate',           cai.rate
                        )
                    ),
                    JSON_ARRAY()
                ) AS slot_options
            FROM weapon                        w
            LEFT JOIN core_slot               cs  ON cs.available_weapon     = w.weapon_id
            LEFT JOIN core_available_item_option cai
                 ON cai.core_type_id           = cs.available_core_type
            LEFT JOIN core_option_detail      cod
                 ON cod.core_option_id         = cai.core_option_id
                AND cod.core_option_grade      = cai.option_grade
            /* plus aucune translation_strings ici */
            WHERE w.weapon_id = p_weapon_id
            GROUP BY w.weapon_id;
        END;
        """
    )
    op.execute("DROP PROCEDURE IF EXISTS GetAllExternalComponents;")
    op.execute(
        """
        /*  SP GetAllExternalComponents()  ───────────────────────────────
            Renvoie pour chaque external_component :

            {
              id, external_component_id,
              external_component_name_id, equipment_type_id, image_url,
              external_component_tier_id,
              base_stat : [ { level, stat_id, stat_value }, … ],
              set_option_detail : [
                 { set_option_id, set_count, set_option_effect_id }, …
              ]
            }
        */
        CREATE PROCEDURE GetAllExternalComponents()
        BEGIN
            /* 1️⃣  Agrégation base-stat par composant ------------------- */
            CREATE TEMPORARY TABLE tmp_stats AS
            SELECT
              ebs.external_component_id,
              JSON_ARRAYAGG(
                 JSON_OBJECT(
                    'level',       ebs.level,
                    'stat_id',     ebs.stat_id,
                    'stat_value',  ebs.stat_value
                 )
                 ORDER BY ebs.level
              ) AS stats_json
            FROM external_component_base_stat ebs
            GROUP BY ebs.external_component_id;

            /* 2️⃣  Agrégation set-bonus par composant ------------------- */
            CREATE TEMPORARY TABLE tmp_sets AS
            SELECT
              ecs.external_component_id,
              JSON_ARRAYAGG(
                 JSON_OBJECT(
                    'set_option_id',        ecs.set_option,
                    'set_count',            ecs.set_count,
                    'set_option_effect_id', ecs.set_option_effect
                 )
              ) AS set_json
            FROM external_component_set_option ecs
            GROUP BY ecs.external_component_id;

            /* 3️⃣  Sélection finale méta + JSON imbriqués --------------- */
            SELECT
              ec.id,
              ec.external_component_id,
              ec.external_component_name_id,
              ec.equipment_type       AS equipment_type_id,
              ec.image_url,
              ec.external_component_tier_id,

              COALESCE(ts.stats_json, JSON_ARRAY()) AS base_stat,
              COALESCE(st.set_json,   JSON_ARRAY()) AS set_option_detail
            FROM external_component ec
              LEFT JOIN tmp_stats ts ON ts.external_component_id = ec.external_component_id
              LEFT JOIN tmp_sets  st ON st.external_component_id = ec.external_component_id
            ORDER BY ec.external_component_id;

            DROP TEMPORARY TABLE tmp_stats;
            DROP TEMPORARY TABLE tmp_sets;
        END
        """
    )
    op.execute("DROP PROCEDURE IF EXISTS GetAllReactors;")
    op.execute(
        """
        CREATE PROCEDURE GetAllReactors()
        BEGIN
            CREATE TEMPORARY TABLE tmp_stats AS
            SELECT
                rc.reactor_id,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'level',      rc.level,
                        'stat_id',    rc.coeff_stat_id,
                        'stat_value', rc.coeff_stat_value
                    )
                    ORDER BY rc.level
                ) AS stats_json
            FROM reactor_coeff rc
            GROUP BY rc.reactor_id;

            SELECT
                r.id,
                r.reactor_id,
                r.reactor_name_id,
                r.optimized_condition_type AS equipment_type_id,
                r.image_url,
                r.reactor_tier_id,

                COALESCE(ts.stats_json, JSON_ARRAY()) AS base_stat,
                JSON_ARRAY() AS set_option_detail
            FROM reactor r
                LEFT JOIN tmp_stats ts ON ts.reactor_id = r.reactor_id
            ORDER BY r.reactor_id;

            DROP TEMPORARY TABLE tmp_stats;
        END
        """
    )
    op.execute("DROP PROCEDURE IF EXISTS GetAllBoards;")
    op.execute(
        """
        CREATE PROCEDURE GetAllBoards()
        BEGIN
            CREATE TEMPORARY TABLE tmp_effects
            AS
            SELECT
                ne.node_id,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                      'stat_id',       ne.stat_id,
                      'stat_value',    ne.stat_value,
                      'operator_type', ne.operator_type
                    )
                ) AS effects_json
            FROM node_effects ne
            GROUP BY ne.node_id;

            CREATE TEMPORARY TABLE tmp_nodes
            AS
            SELECT
                bn.board_id,                 /* ← référence à boards.id */
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                      'node_id',               n.node_id,
                      'name_id',               n.name_id,
                      'image_url',             n.image_url,
                      'node_type',             n.node_type,
                      'tier_id',               n.tier_id,
                      'required_tuning_point', n.required_tuning_point,
                      'position_row',          bn.position_row,
                      'position_column',       bn.position_column,
                      'effects',               COALESCE(te.effects_json, JSON_ARRAY())
                    )
                ) AS nodes_json
            FROM board_nodes bn
            JOIN nodes      n  ON n.node_id = bn.node_id
            LEFT JOIN tmp_effects te ON te.node_id = n.node_id
            GROUP BY bn.board_id;

            SELECT
                b.id,                         -- clé DB
                b.arche_tuning_board_id,      -- identifiant métier
                b.row_size,
                b.column_size,
                COALESCE(tn.nodes_json, JSON_ARRAY()) AS nodes
            FROM boards b
            LEFT JOIN tmp_nodes tn ON tn.board_id = b.id
            ORDER BY b.arche_tuning_board_id;

            DROP TEMPORARY TABLE tmp_effects;
            DROP TEMPORARY TABLE tmp_nodes;
        END
        """
    )

def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS GetAllExternalComponents;")
    op.execute("DROP PROCEDURE IF EXISTS GetAllTranslations;")
    op.execute("DROP PROCEDURE IF EXISTS GetWeaponCoreSlots;")
    op.execute("DROP PROCEDURE IF EXISTS GetAllDescendants;")
    op.execute("DROP PROCEDURE IF EXISTS GetAllReactors;")
    op.execute("DROP PROCEDURE IF EXISTS GetAllModules;")
    op.execute("DROP PROCEDURE IF EXISTS GetAllWeapons;")
    op.execute("DROP PROCEDURE IF EXISTS GetAllBoards;")
    op.execute("DROP PROCEDURE IF EXISTS GetAllCores;")

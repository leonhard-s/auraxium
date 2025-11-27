====================
Collection Reference
====================

=====================================  ==================================================================  ================================================================================================
Census Collection                      Auraxium                                                            Comment
=====================================  ==================================================================  ================================================================================================
``ability``                            :class:`auraxium.ps2.Ability`                                       --
``ability_type``                       :class:`auraxium.ps2.AbilityType`                                   --
``achievement``                        :class:`auraxium.ps2.Achievement`                                   --
``armor_facing``                       :class:`auraxium.ps2.ArmourFacing`                                  --
``armor_info``                         :class:`auraxium.ps2.ArmourInfo`                                    --
``character``                          :class:`auraxium.ps2.Character`                                     --
``character_name``                     --                                                                  Optimised way of resolving character names. Used internally where applicable.
``characters_achievement``             :meth:`auraxium.ps2.Character.achievements`                         --
``characters_currency``                :meth:`auraxium.ps2.Character.currency`                             --
``characters_directive``               :meth:`auraxium.ps2.Character.directive`                            --
``characters_directive_objective``     :meth:`auraxium.ps2.Character.directive_objective`                  --
``characters_directive_tier``          :meth:`auraxium.ps2.Character.directive_tier`                       --
``characters_directive_tree``          :meth:`auraxium.ps2.Character.directive_tree`                       --
``characters_event``                   :meth:`auraxium.ps2.Character.events`                               --
``characters_event_grouped``           :meth:`auraxium.ps2.Character.events_grouped`                       --
``characters_friend``                  :meth:`auraxium.ps2.Character.friends`                              --
``characters_item``                    :meth:`auraxium.ps2.Character.items`                                 --
``characters_leaderboard``             :func:`auraxium.ps2.leaderboard.by_char`                            --
``characters_online_status``           :meth:`auraxium.ps2.Character.online_status`                        --
``characters_skill``                   :meth:`auraxium.ps2.Character.skill`                                --
``characters_stat``                    :meth:`auraxium.ps2.Character.stat`                                 --
``characters_stat_by_faction``         :meth:`auraxium.ps2.Character.stat_by_faction`                      --
``characters_stat``                    :meth:`auraxium.ps2.Character.stat`                                 --
``characters_stat_history``            :meth:`auraxium.ps2.Character.stat_history`                         --
``characters_skill``                   :meth:`auraxium.ps2.Character.skill`                                --
``characters_weapon_stat``             :meth:`auraxium.ps2.Character.weapon_stat`                          --
``characters_weapon_stat_by_faction``  :meth:`auraxium.ps2.Character.weapon_stat_by_faction`               --
``characters_world``                   :meth:`auraxium.ps2.Character.world`                                --
``currency``                           :class:`auraxium.ps2.Currency`                                      --
``directive``                          :class:`auraxium.ps2.Directive`                                     --
``directive_tier``                     :class:`auraxium.ps2.DirectiveTier`                                 --
``directive_tree``                     :class:`auraxium.ps2.DirectiveTree`                                 --
``directive_tree_category``            :class:`auraxium.ps2.DirectiveTreeCategory`                         --
``effect``                             :class:`auraxium.ps2.Effect`                                        --
``effect_type``                        :class:`auraxium.ps2.EffectType`                                    --
``empire_scores``                      --                                                                  Unused
``experience``                         :class:`auraxium.ps2.Experience`                                    --
``experience_award_type``              :class:`auraxium.ps2.ExperienceAwardType`                           --
``experience_rank``                    :class:`auraxium.ps2.ExperienceRank`                                --
``event``                              --                                                                  Not yet implemented
``facility_link``                      :meth:`auraxium.ps2.MapRegion.get_connected`                        --
``facility_type``                      :class:`auraxium.ps2.FacilityType`                                  --
``faction``                            :class:`auraxium.ps2.Faction`                                       --
``fire_group``                         :class:`auraxium.ps2.FireGroup`                                     --
``fire_group_to_fire_mode``            :meth:`auraxium.ps2.FireGroup.fire_modes`                           --
``fire_mode``                          --                                                                  Superceded by ``fire_mode_2``
``fire_mode_2``                        :class:`auraxium.ps2.FireMode`                                      --
``fire_mode_to_projectile``            :meth:`auraxium.ps2.FireMode.projectile`                            --
``fire_mode_type``                     :class:`auraxium.ps2.FireModeType`                                  --
``fish``                               :class:`auraxium.ps2.Fish`                                          --
``image``                              --                                                                  Not yet implemented
``image_set``                          --                                                                  Not yet implemented
``image_set_default``                  --                                                                  Not yet implemented
``item``                               :class:`auraxium.ps2.Item`                                          --
``item_attachment``                    :meth:`auraxium.ps2.Item.attachments`                               --
``item_category``                      :class:`auraxium.ps2.ItemCategory`                                  --
``item_profile``                       :meth:`auraxium.ps2.Item.profiles`                                  --
``item_to_weapon``                     :meth:`auraxium.ps2.Item.weapon`, :meth:`auraxium.ps2.Weapon.item`  --
``item_type``                          :class:`auraxium.ps2.ItemType`                                      --
``leaderboard``                        :mod:`auraxium.ps2.leaderboard`                                     --
``loadout``                            :class:`auraxium.ps2.Loadout`                                       --
``map``                                :meth:`auraxium.ps2.World.map`                                      --
``map_hex``                            :class:`auraxium.ps2.MapHex`                                        --
``map_region``                         :class:`auraxium.ps2.MapRegion`                                     --
``marketing_bundle``                   :class:`auraxium.ps2.MarketingBundle`                               --
``marketing_bundle_item``              :meth:`auraxium.ps2.MarketingBundle.items`                          --
``marketing_bundle_with_1_item``       :class:`auraxium.ps2.MarketingBundleSingle`                         --
``metagame_event``                     :class:`auraxium.ps2.MetagameEvent`                                 --
``metagame_event_state``               :class:`auraxium.ps2.MetagameEventState`                            --
``objective``                          :class:`auraxium.ps2.Objective`                                     --
``objective_set_to_objective``         :meth:`auraxium.ps2.Directive.objectives`                           --
``objective_type``                     :class:`auraxium.ps2.ObjectiveType`                                  --
``outfit``                             :class:`auraxium.ps2.Outfit`                                        --
``outfit_member``                      :class:`auraxium.ps2.OutfitMember`                                  --
``outfit_member_extended``             --                                                                  Join of ``outfit_member`` and ``outfit``
``outfit_rank``                        :meth:`auraxium.ps2.Outfit.ranks`                                   --
``player_state``                       :class:`auraxium.ps2.PlayerState`                                   --
``player_state_group``                 --                                                                  Superceded by ``player_state_group_2``
``player_state_group_2``               :class:`auraxium.collections.PlayerStateGroup`                      --
``profile``                            --                                                                  Superceded by ``profile_2``
``profile_2``                          :class:`auraxium.ps2.Profile`                                       --
``profile_armor_map``                  :meth:`auraxium.ps2.Profile.armour_info`                            --
``profile_resist_map``                 :meth:`auraxium.ps2.Profile.resist_info`                            --
``projectile``                         :class:`auraxium.ps2.Projectile`                                    --
``projectile_flight_type``             :class:`auraxium.ps2.ProjectileFlightType`                          --
``region``  	                       :class:`auraxium.ps2.Region`                                        --
``resist_info``                        :class:`auraxium.ps2.ResistInfo`                                    --
``resist_type``                        :class:`auraxium.ps2.ResistType`                                    --
``resource_type``                      :class:`auraxium.ps2.ResourceType`                                  --
``reward``                             :class:`auraxium.ps2.Reward`                                        --
``reward_group_to_reward``             :meth:`auraxium.ps2.Reward.get_by_reward_group`                     --
``reward_type``                        :class:`auraxium.ps2.RewardType`                                    --
``reward_set_to_reward_group``         :meth:`auraxium.ps2.Reward.get_by_reward_group`                     --
``single_character_by_id``             --                                                                  Optimised way of accessing bulk data related to ``character``. Used internally where applicable.
``skill``                              :class:`auraxium.ps2.Skill`                                         --
``skill_category``                     :class:`auraxium.ps2.SkillCategory`                                 --
``skill_line``                         :class:`auraxium.ps2.SkillLine`                                     --
``skill_set``                          :class:`auraxium.ps2.SkillSet`                                      --
``target_type``                        :class:`auraxium.ps2.TargetType`                                    --
``title``                              :class:`auraxium.ps2.Title`                                         --
``vehicle``                            :class:`auraxium.ps2.Vehicle`                                       --
``vehicle_attachment``                 :class:`auraxium.ps2.VehicleAttachment`                             --
``vehicle_faction``                    :meth:`auraxium.ps2.Vehicle.factions`                               --
``vehicle_skill_set``                  :meth:`auraxium.ps2.Vehicle.skill_sets`                             --
``weapon``                             :class:`auraxium.ps2.Weapon`                                        --
``weapon_ammo_slot``                   :meth:`auraxium.ps2.Weapon.ammo_slots`                              --
``weapon_datasheet``                   :meth:`auraxium.ps2.Weapon.datasheet`                               --
``weapon_to_attachment``               :meth:`auraxium.ps2.Weapon.attachments`                             --
``weapon_to_fire_group``               :meth:`auraxium.ps2.Weapon.fire_groups`                             --
``world``                              :class:`auraxium.ps2.World`                                         --
``world_event``                        --                                                                  Unused
``world_stat_history``                 --                                                                  Unused
``zone``                               :class:`auraxium.ps2.Zone`                                          --
``zone_effect``                        :class:`auraxium.ps2.ZoneEffect`                                    --
``zone_effect_type``                   :class:`auraxium.ps2.ZoneEffectType`                                --
=====================================  ==================================================================  ================================================================================================

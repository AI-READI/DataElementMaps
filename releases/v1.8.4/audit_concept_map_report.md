# Concept map audit

Source: `_ai_readi_redcap_value_set_mapping_common.csv` (2143 data rows)
Part A checks marked *expect 0* should report no rows. Parts B and C are review lists.
Vocabulary checks (standard, valid, name match in the deployed `omop_vocab`) are in `validate_concept_map_vocab.sql`.

## A1 Custom targets vs concept_manual.csv: 0 (expect 0)

## A2 Same concept_id with different name/domain/vocabulary/code: 0 (expect 0)

## A3 Non-custom target not flagged standard: 0 (expect 0)

## A4 Predicate / confidence rules: 0 (expect 0)

## A5 Duplicate keys (informational: Yes -> Condition/Observation/Procedure + Yes value pairs are expected): 79
| Form / field / code / type | Lines | Targets |
|---|---|---|
| ecg /  / rtekgcmpdattim / Question | 286, 2139 | 4160030 Performed (Observation) \| 4145308 12 lead ECG (Procedure) |
| health_survey / mhoccur_mi / 1 / Answer | 328, 440 | 4329847 Myocardial infarction (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_cvdot / 1 / Answer | 337, 441 | 2005200627 Other heart issues (Examples: pacemaker, (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_strk / 1 / Answer | 340, 443 | 381316 Cerebrovascular accident (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_circ / 1 / Answer | 343, 444 | 2005200015 Circulation problems (Examples: arterios (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_clsh / 1 / Answer | 346, 478 | 4029305 Hypercholesterolemia (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_hbp / 1 / Answer | 349, 479 | 316866 Hypertensive disorder (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_lbp / 1 / Answer | 352, 480 | 317002 Low blood pressure (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_pd / 1 / Answer | 355, 481 | 381270 Parkinson's disease (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_ad / 1 / Answer | 358, 482 | 4182210 Dementia (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_cogn / 1 / Answer | 365, 483 | 4297400 Mild neurocognitive disorder (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_ms / 1 / Answer | 368, 484 | 374919 Multiple sclerosis (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_cns / 1 / Answer | 371, 485 | 376337 Disorder of nervous system (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_ra / 1 / Answer | 374, 486 | 4291025 Arthritis (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_oa / 1 / Answer | 377, 487 | 80502 Osteoporosis (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_ca / 1 / Answer | 380, 488 | 443392 Malignant neoplastic disease (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_plm / 1 / Answer | 383, 489 | 4186898 Chronic lung disease (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_gi / 1 / Answer | 386, 490 | 4201745 Disorder of digestive system (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_ua / 1 / Answer | 389, 491 | 75865 Disorder of urinary system (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_rnl / 1 / Answer | 392, 492 | 198124 Kidney disease (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_ear / 1 / Answer | 395, 493 | 377889 Hearing loss (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_obs / 1 / Answer | 398, 494 | 433736 Obesity (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_glc / 1 / Answer | 415, 495 | 437541 Glaucoma (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_amd / 1 / Answer | 418, 496 | 374028 Age related macular degeneration (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_crt / 1 / Answer | 421, 497 | 375545 Cataract (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_pdr / 1 / Answer | 424, 498 | 4174977 Retinopathy due to diabetes mellitus (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_rvo / 1 / Answer | 427, 499 | 440392 Retinal vascular occlusion (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_ded / 1 / Answer | 430, 500 | 4036620 Dry eyes (Condition) \| 45877994 Yes (Meas Value) |
| health_survey / mhoccur_yn / 1 / Answer | 433, 501 | 46234759 Other health condition (Observation) \| 45877994 Yes (Meas Value) |
| physical_assessment / paate_6hr / 1 / Answer | 868, 871 | 44792839 Non fasting (Observation) \| 45877994 Yes (Meas Value) |
| physical_assessment / paate_6hr / 0 / Answer | 869, 872 | 4060364 Fasting (Observation) \| 45878245 No (Meas Value) |
| retinal_imaging_v2 / rtop_odd / 1 / Answer | 1743, 2081 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtop_odm / 1 / Answer | 1745, 2082 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtei_odir / 1 / Answer | 1747, 2083 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtei_odfaf / 1 / Answer | 1749, 2084 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtsm_odc / 1 / Answer | 1767, 2085 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtsm_odn / 1 / Answer | 1769, 2086 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtsm_odt / 1 / Answer | 1771, 2087 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtsm_odm / 1 / Answer | 1773, 2088 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtso_odo / 1 / Answer | 1775, 2089 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtso_odp / 1 / Answer | 1777, 2090 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtso_odm / 1 / Answer | 1779, 2091 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rtci_odm1 / 1 / Answer | 1781, 2092 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtci_odd1 / 1 / Answer | 1783, 2093 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtci_odm2 / 1 / Answer | 1785, 2094 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rtci_odd2 / 1 / Answer | 1787, 2095 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rtma_odw / 1 / Answer | 1789, 2096 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtma_odm / 1 / Answer | 1791, 2097 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtma_odm1 / 1 / Answer | 1793, 2098 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rttr_odr / 1 / Answer | 1795, 2099 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rttr_odm1 / 1 / Answer | 1797, 2100 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rttr_odm2 / 1 / Answer | 1799, 2101 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rtfl_od / 1 / Answer | 1801, 2102 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtop_osd / 1 / Answer | 1803, 2103 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtop_osm / 1 / Answer | 1805, 2104 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtei_osir / 1 / Answer | 1807, 2105 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtei_osfaf / 1 / Answer | 1809, 2106 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtsm_osc / 1 / Answer | 1811, 2107 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtsm_osn / 1 / Answer | 1813, 2108 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtsm_ost / 1 / Answer | 1815, 2109 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtsm_osm / 1 / Answer | 1817, 2110 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| retinal_imaging_v2 / rtso_oso / 1 / Answer | 1819, 2111 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtso_osp / 1 / Answer | 1821, 2112 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtso_osm / 1 / Answer | 1823, 2113 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rtci_osm1 / 1 / Answer | 1825, 2114 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtci_osd1 / 1 / Answer | 1827, 2115 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtci_osm2 / 1 / Answer | 1829, 2116 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rtci_osd2 / 1 / Answer | 1831, 2117 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rtma_osw / 1 / Answer | 1833, 2118 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtma_osm / 1 / Answer | 1835, 2119 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rtma_osm1 / 1 / Answer | 1837, 2120 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rttr_osr / 1 / Answer | 1839, 2121 | 45877994 Yes (Meas Value) \| 1073298 Optical coherence tomography of posterio (Procedure) |
| retinal_imaging_v2 / rttr_osm1 / 1 / Answer | 1841, 2122 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rttr_osm2 / 1 / Answer | 1843, 2123 | 45877994 Yes (Meas Value) \| 745759 Computerized ophthalmic diagnostic imagi (Procedure) |
| retinal_imaging_v2 / rtfl_os / 1 / Answer | 1845, 2124 | 45877994 Yes (Meas Value) \| 4063911 Ocular fundus photography (Procedure) |
| screening_survey / mhterm_dm1 / 1 / Answer | 1861, 1867 | 45877994 Yes (Meas Value) \| 201254 Type 1 diabetes mellitus (Condition) |
| screening_survey / mhterm_dm2 / 1 / Answer | 1863, 1864 | 201826 Type 2 diabetes mellitus (Condition) \| 45877994 Yes (Meas Value) |
| screening_survey / mhterm_predm / 1 / Answer | 1865, 1868 | 45877994 Yes (Meas Value) \| 37018196 Prediabetes (Condition) |
| screening_survey / mh_a1c / 1 / Answer | 1866, 1869 | 45877994 Yes (Meas Value) \| 4214376 Hyperglycemia (Condition) |

## A6 Leading/trailing or non-breaking spaces: 0 (expect 0)

## A7 Custom concepts used as Condition targets (check for a standard alternative): 2
| Line | FIELD_ID | SRC_CODE | Source text | Concept | Name |
|---|---|---|---|---|---|
| 337 | mhoccur_cvdot | 1 | Yes | 2005200627 | Other heart issues (Examples: pacemaker, heart valve disease |
| 343 | mhoccur_circ | 1 | Yes | 2005200015 | Circulation problems (Examples: arteriosclerosis, atheroscle |

## A8 Answers whose FIELD_ID matches no question row (field-name typos; administrative fields expected): 3
| Line | Form | FIELD_ID | SRC_CODE | Source text | Concept |
|---|---|---|---|---|---|
| 39 | bcva | viaodnd | 1 | Not done |  |
| 40 | bcva | viaosnd | 1 | Not done |  |
| 131 | device_return | send_satisfaction_survey | 1 | Checking the box and saving the form schedules a survey invi |  |

## B1 Answers whose text differs from the target name (review each): 342
| Line | FIELD_ID | SRC_CODE | Source text | Concept | Target name | Domain | Predicate |
|---|---|---|---|---|---|---|---|
| 34 | viaomthd | 2 | ETDRS | 4268147 | ETDRS visual acuity chart | Device | exactMatch 1 |
| 119 | cl_maristat | C51777 | Living separately but not divorced | 45884459 | Separated | Meas Value | exactMatch 1 |
| 137 | dvamwendhand | 1 | Right hand | 45881626 | Right | Meas Value | exactMatch 1 |
| 138 | dvamwendhand | 2 | Left hand | 45883143 | Left | Meas Value | exactMatch 1 |
| 139 | dvamwendhand | 4 | Neither (ambidextrous) | 4045863 | Ambidextrous | Observation | exactMatch 1 |
| 156 | dmlvex | 0 | Rarely or none | 45883771 | Rarely or never | Meas Value | exactMatch 1 |
| 164 | dmlhex | 0 | Rarely or none | 45883771 | Rarely or never | Meas Value | exactMatch 1 |
| 180 | dmlfrveg | 0 | Rarely or none | 45883771 | Rarely or never | Meas Value | exactMatch 1 |
| 184 | dmledu | 0 | Rarely or none | 45883771 | Rarely or never | Meas Value | exactMatch 1 |
| 186 | dmlfeet | 10 | Daily or weekly | 45879676 | Daily or almost daily | Meas Value | closeMatch 0.75 |
| 188 | dmlfeet | 0 | Rarely or none | 45883771 | Rarely or never | Meas Value | exactMatch 1 |
| 250 | eos_dsdecod | 1 | Did not meet Inclusion/Exclusion criteria | 40480675 | Does not meet eligibility criteria for clinical trial | Observation | exactMatch 1 |
| 259 | eos_dsdecod | 888 | Other {eos_dsterm} | 45878142 | Other | Meas Value | exactMatch 1 |
| 261 | eos_dsdecodie | 2 | Individual is pregnant | 45884583 | Currently pregnant | Meas Value | closeMatch 1 |
| 265 | eos_dsvst | 0 | Signed Consent | 3018196 | Informed consent obtained | Observation | closeMatch 1 |
| 266 | eos_dsvst | 1 | Pre-Visit | 35626257 | Before appointment | Meas Value | closeMatch 0.75 |
| 328 | mhoccur_mi | 1 | Yes | 4329847 | Myocardial infarction | Condition | exactMatch 1 |
| 340 | mhoccur_strk | 1 | Yes | 381316 | Cerebrovascular accident | Condition | exactMatch 1 |
| 346 | mhoccur_clsh | 1 | Yes | 4029305 | Hypercholesterolemia | Condition | exactMatch 1 |
| 349 | mhoccur_hbp | 1 | Yes | 316866 | Hypertensive disorder | Condition | exactMatch 1 |
| 352 | mhoccur_lbp | 1 | Yes | 317002 | Low blood pressure | Condition | exactMatch 1 |
| 355 | mhoccur_pd | 1 | Yes | 381270 | Parkinson's disease | Condition | exactMatch 1 |
| 358 | mhoccur_ad | 1 | Yes | 4182210 | Dementia | Condition | exactMatch 1 |
| 363 | mhcat_adot | 999 | Unsure from the options listed | 45882025 | Unsure | Meas Value | exactMatch 1 |
| 365 | mhoccur_cogn | 1 | Yes | 4297400 | Mild neurocognitive disorder | Condition | exactMatch 1 |
| 368 | mhoccur_ms | 1 | Yes | 374919 | Multiple sclerosis | Condition | exactMatch 1 |
| 371 | mhoccur_cns | 1 | Yes | 376337 | Disorder of nervous system | Condition | closeMatch 0.75 |
| 374 | mhoccur_ra | 1 | Yes | 4291025 | Arthritis | Condition | exactMatch 1 |
| 377 | mhoccur_oa | 1 | Yes | 80502 | Osteoporosis | Condition | exactMatch 1 |
| 380 | mhoccur_ca | 1 | Yes | 443392 | Malignant neoplastic disease | Condition | exactMatch 1 |
| 383 | mhoccur_plm | 1 | Yes | 4186898 | Chronic lung disease | Condition | exactMatch 1 |
| 386 | mhoccur_gi | 1 | Yes | 4201745 | Disorder of digestive system | Condition | exactMatch 1 |
| 389 | mhoccur_ua | 1 | Yes | 75865 | Disorder of urinary system | Condition | closeMatch 0.75 |
| 392 | mhoccur_rnl | 1 | Yes | 198124 | Kidney disease | Condition | closeMatch 0.75 |
| 395 | mhoccur_ear | 1 | Yes | 377889 | Hearing loss | Condition | exactMatch 1 |
| 398 | mhoccur_obs | 1 | Yes | 433736 | Obesity | Condition | exactMatch 1 |
| 401 | fh_dm2pt | 1 | Yes | 4334340 | Family history of diabetes mellitus type 2 | Observation | exactMatch 1 |
| 407 | fh_dm2sb | 1 | Yes | 4334340 | Family history of diabetes mellitus type 2 | Observation | exactMatch 1 |
| 415 | mhoccur_glc | 1 | Yes | 437541 | Glaucoma | Condition | exactMatch 1 |
| 418 | mhoccur_amd | 1 | Yes | 374028 | Age related macular degeneration | Condition | exactMatch 1 |
| 421 | mhoccur_crt | 1 | Yes | 375545 | Cataract | Condition | exactMatch 1 |
| 424 | mhoccur_pdr | 1 | Yes | 4174977 | Retinopathy due to diabetes mellitus | Condition | exactMatch 1 |
| 427 | mhoccur_rvo | 1 | Yes | 440392 | Retinal vascular occlusion | Condition | exactMatch 1 |
| 430 | mhoccur_ded | 1 | Yes | 4036620 | Dry eyes | Condition | exactMatch 1 |
| 433 | mhoccur_yn | 1 | Yes | 46234759 | Other health condition | Observation | exactMatch 1 |
| 437 | mhoccur_fall | 1 | Yes | 40757198 | Falls in the past year | Observation | exactMatch 1 |
| 451 | ethnic | C67113 | Yes, Mexican | 45878460 | Mexican | Meas Value | exactMatch 1 |
| 452 | ethnic | C67112 | Yes, Puerto Rican | 45878458 | Puerto Rican | Meas Value | exactMatch 1 |
| 453 | ethnic | C107608 | Yes, Cuban | 45880060 | Cuban | Meas Value | exactMatch 1 |
| 454 | ethnic | C67117 | Yes, Dominican Republic | 45884241 | Dominican Republic | Meas Value | exactMatch 1 |
| 455 | ethnic | C67118 | Yes, Central American | 45884898 | Central American | Meas Value | exactMatch 1 |
| 456 | ethnic | C126532 | Yes, South American | 45880479 | South American | Meas Value | exactMatch 1 |
| 457 | ethnic | C999 | Yes, Chicano | 45884418 | Chicano | Meas Value | exactMatch 1 |
| 458 | ethnic | 888 | Yes, Other | 45878142 | Other | Meas Value | exactMatch 1 |
| 464 | race | C41219 | Native Hawaiian or Pacific Islander | 45878240 | Native Hawaiian or Other Pacific Islander | Meas Value | exactMatch 1 |
| 466 | race | C41261 | White or Caucasian | 45877987 | White | Meas Value | exactMatch 1 |
| 467 | race | 888 | Other race, ethnicity or origin | 45878142 | Other | Meas Value | exactMatch 1 |
| 475 | race2 | C41261 | White or Caucasian | 45877987 | White | Meas Value | exactMatch 1 |
| 476 | race2 | 888 | Other race, ethnicity or origin | 45878142 | Other | Meas Value | exactMatch 1 |
| 690 | cm_asp | 2 | A few days (<1 day/week) | 36210209 | Less than once a week | Meas Value | exactMatch 1 |
| 691 | cm_asp | 3 | Some days (1-2 days/week) | 1620467 | A few days (1-2 days) | Meas Value | closeMatch 1 |
| 692 | cm_asp | 4 | Most days (3-4 days/week) | 1620862 | Most days (3-4 days) | Meas Value | closeMatch 1 |
| 693 | cm_asp | 99 | Don't know/not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 694 | cm_asp | 777 | Decline to answer | 36311156 | Prefer not to say | Meas Value | exactMatch 1 |
| 697 | cm_act | 2 | A few days (<1 day/week) | 36210209 | Less than once a week | Meas Value | exactMatch 1 |
| 698 | cm_act | 3 | Some days (1-2 days/week) | 1620467 | A few days (1-2 days) | Meas Value | closeMatch 1 |
| 699 | cm_act | 4 | Most days (3-4 days/week) | 1620862 | Most days (3-4 days) | Meas Value | closeMatch 1 |
| 700 | cm_act | 99 | Don't know/not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 701 | cm_act | 777 | Decline to answer | 36311156 | Prefer not to say | Meas Value | exactMatch 1 |
| 704 | cm_ibp | 2 | A few days (<1 day/week) | 36210209 | Less than once a week | Meas Value | exactMatch 1 |
| 705 | cm_ibp | 3 | Some days (1-2 days/week) | 1620467 | A few days (1-2 days) | Meas Value | closeMatch 1 |
| 706 | cm_ibp | 4 | Most days (3-4 days/week) | 1620862 | Most days (3-4 days) | Meas Value | closeMatch 1 |
| 707 | cm_ibp | 99 | Don't know/not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 708 | cm_ibp | 777 | Decline to answer | 36311156 | Prefer not to say | Meas Value | exactMatch 1 |
| 711 | cm_ant | 2 | A few days (<1 day/week) | 36210209 | Less than once a week | Meas Value | exactMatch 1 |
| 712 | cm_ant | 3 | Some days (1-2 days/week) | 1620467 | A few days (1-2 days) | Meas Value | closeMatch 1 |
| 713 | cm_ant | 4 | Most days (3-4 days/week) | 1620862 | Most days (3-4 days) | Meas Value | closeMatch 1 |
| 714 | cm_ant | 99 | Don't know/not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 715 | cm_ant | 777 | Decline to answer | 36311156 | Prefer not to say | Meas Value | exactMatch 1 |
| 718 | cm_dcg | 2 | A few days (<1 day/week) | 36210209 | Less than once a week | Meas Value | exactMatch 1 |
| 719 | cm_dcg | 3 | Some days (1-2 days/week) | 1620467 | A few days (1-2 days) | Meas Value | closeMatch 1 |
| 720 | cm_dcg | 4 | Most days (3-4 days/week) | 1620862 | Most days (3-4 days) | Meas Value | closeMatch 1 |
| 721 | cm_dcg | 99 | Don't know/not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 722 | cm_dcg | 777 | Decline to answer | 36311156 | Prefer not to say | Meas Value | exactMatch 1 |
| 725 | cm_slp | 2 | A few days (<1 day/week) | 36210209 | Less than once a week | Meas Value | exactMatch 1 |
| 726 | cm_slp | 3 | Some days (1-2 days/week) | 1620467 | A few days (1-2 days) | Meas Value | closeMatch 1 |
| 727 | cm_slp | 4 | Most days (3-4 days/week) | 1620862 | Most days (3-4 days) | Meas Value | closeMatch 1 |
| 728 | cm_slp | 99 | Don't know/not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 729 | cm_slp | 777 | Decline to answer | 36311156 | Prefer not to say | Meas Value | exactMatch 1 |
| 779 | via1 | 5 | Unable to do because of eyesight | 45879202 | Stopped doing this because of your eyesight | Meas Value | exactMatch 1 |
| 785 | via2 | 5 | Unable to do because of eyesight | 45879202 | Stopped doing this because of your eyesight | Meas Value | exactMatch 1 |
| 791 | via3 | 5 | Unable to do because of eyesight | 45879202 | Stopped doing this because of your eyesight | Meas Value | exactMatch 1 |
| 793 | via4 | 1 | Within the past month (anytime less than 1 month ago) | 45882114 | Within 30 days | Meas Value | closeMatch 1 |
| 794 | via4 | 2 | Within the past year (1 month but less than 12 months ago) | 45883457 | More than 30 days ago but within the past 12 months | Meas Value | exactMatch 1 |
| 796 | via4 | 4 | 2 or more years ago | 1990160 | More than 2 years ago (more than 105 weeks ago) | Meas Value | closeMatch 1 |
| 806 | via6 | 1 | Within the past month (anytime less than 1 month ago) | 45882114 | Within 30 days | Meas Value | closeMatch 1 |
| 807 | via6 | 2 | Within the past year (1 month but less than 12 months ago) | 45883457 | More than 30 days ago but within the past 12 months | Meas Value | exactMatch 1 |
| 809 | via6 | 4 | 2 or more years ago | 1990160 | More than 2 years ago (more than 105 weeks ago) | Meas Value | closeMatch 1 |
| 868 | paate_6hr | 1 | Yes | 44792839 | Non fasting | Observation | exactMatch 1 |
| 869 | paate_6hr | 0 | No | 4060364 | Fasting | Observation | exactMatch 1 |
| 935 | pxne1 | 2 | Townhouses, row houses, apartments, or condos of 2-3 stories | 45876908 | Townhouses, row houses, apartments, or condos of two-three stories | Meas Value | exactMatch 1 |
| 939 | pxne1 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 945 | pxne2 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 951 | pxne3 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 958 | pxne4 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 965 | pxne5 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 970 | pxhic6 | 0 | Not Covered | 45881114 | Not Covered by Insurance | Meas Value | exactMatch 1 |
| 975 | pxne6 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 981 | pxne7 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 988 | pxne8 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 994 | pxne9 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 1000 | pxne10 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 1004 | pxne11 | 555 | Don't know / unsure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 1011 | pxne12 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 1017 | pxne13 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 1023 | pxne14 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 1029 | pxne15 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 1035 | pxne16 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 1041 | pxne17 | 555 | Don't know/Not sure | 45876636 | Don't know | Meas Value | exactMatch 1 |
| 1102 | pxrd1 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1106 | pxrd1 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1109 | pxrd2 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1113 | pxrd2 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1115 | pxrd3 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1116 | pxrd3 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1119 | pxrd4 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1123 | pxrd4 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1126 | pxrd5 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1130 | pxrd5 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1132 | pxrd6 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1133 | pxrd6 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1136 | pxrd7 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1140 | pxrd7 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1143 | pxrd8 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1147 | pxrd8 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1149 | pdrx9 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1150 | pdrx9 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1153 | pxrd10 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1157 | pxrd10 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1160 | pxrd11 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1164 | pxrd11 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1166 | pxrd12 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1167 | pxrd12 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1170 | pxrd13 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1174 | pxrd13 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1177 | pxrd14 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1181 | pxrd14 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1183 | pxrd15 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1184 | pxrd15 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1187 | pxrd16 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1191 | pxrd16 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1194 | pxrd17 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1198 | pxrd17 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1200 | pxrd18 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1201 | pxrd18 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1204 | pxrd19 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1208 | pxrd19 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1211 | pxrd20 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1215 | pxrd20 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1217 | pxrd21 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1218 | pxrd21 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1221 | pxrd22 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1225 | pxrd22 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1228 | pxrd23 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1232 | pxrd23 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1234 | pxrd24 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1235 | pxrd24 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1238 | pxrd25 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1242 | pxrd25 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1245 | pxrd26 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1249 | pxrd26 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1251 | pxrd27 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1252 | pxrd27 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1255 | pxrd28 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1259 | pxrd28 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1262 | pxrd29 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1266 | pxrd29 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1268 | pxrd30 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1269 | pxrd30 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1272 | pxrd31 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1276 | pxrd31 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1279 | pxrd32 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1283 | pxrd32 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1285 | pxrd33 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1286 | pxrd33 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1289 | pxrd34 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1293 | pxrd34 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1296 | pxrd35 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1300 | pxrd35 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1302 | pxrd36 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1303 | pxrd36 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1306 | pxrd37 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1310 | pxrd37 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1313 | pxrd38 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1317 | pxrd38 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1319 | pxrd39 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1320 | pxrd39 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1323 | pxrd40 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1327 | pxrd40 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1330 | pxrd41 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1334 | pxrd41 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1336 | pxrd42 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1337 | pxrd42 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1340 | pxrd43 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1344 | pxrd43 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1347 | pxrd44 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1351 | pxrd44 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1353 | pxrd45 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1354 | pxrd45 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1357 | pxrd46 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1361 | pxrd46 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1364 | pxrd47 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1368 | pxrd47 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1370 | pxrd48 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1371 | pxrd48 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1374 | pxrd49 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1378 | pxrd49 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1381 | pxrd50 | 2 | Once in a while | 45879593 | Occasionally | Meas Value | closeMatch 1 |
| 1385 | pxrd50 | 6 | Almost all the time | 45883838 | All the time | Meas Value | closeMatch 1 |
| 1387 | pxrd51 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1388 | pxrd51 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1390 | pxrd52 | 1 | The Same as it is now | 45879534 | About the same | Meas Value | closeMatch 0.75 |
| 1391 | pxrd52 | 2 | A little different | 45880786 | Slight change | Meas Value | closeMatch 0.75 |
| 1392 | pxrd52 | 3 | Different in a few ways | 45880786 | Slight change | Meas Value | closeMatch 0.75 |
| 1393 | pxrd52 | 4 | Different in a lot of ways | 45877440 | Major change | Meas Value | closeMatch 0.75 |
| 1394 | pxrd52 | 5 | Different in most ways | 45877440 | Major change | Meas Value | closeMatch 0.75 |
| 1395 | pxrd52 | 6 | Totally different | 45877440 | Major change | Meas Value | closeMatch 0.75 |
| 1397 | pxrd53 | 1 | The Same as it is now | 45879534 | About the same | Meas Value | closeMatch 0.75 |
| 1398 | pxrd53 | 2 | A little different | 45880786 | Slight change | Meas Value | closeMatch 0.75 |
| 1399 | pxrd53 | 3 | Different in a few ways | 45880786 | Slight change | Meas Value | closeMatch 0.75 |
| 1400 | pxrd53 | 4 | Different in a lot of ways | 45877440 | Major change | Meas Value | closeMatch 0.75 |
| 1401 | pxrd53 | 5 | Different in most ways | 45877440 | Major change | Meas Value | closeMatch 0.75 |
| 1402 | pxrd53 | 6 | Totally different | 45877440 | Major change | Meas Value | closeMatch 0.75 |
| 1404 | pxrd54 | 1 | 1 - Not at all stressful | 36210226 | Not at all bothersome | Meas Value | closeMatch 1 |
| 1405 | pxrd54 | 6 | 6 - Extremely stressful | 36210124 | Extremely bothersome | Meas Value | closeMatch 1 |
| 1458 | pxep2 | 1 | Yes | 37079013 | Language other than English | Meas Value | closeMatch 1 |
| 1485 | pxed1 | 18 | Bachelor's Degree (Example: BA, AB, BS, BBA) | 45884155 | Bachelor's degree (e.g., BA, AB, BS) | Meas Value | exactMatch 1 |
| 1486 | pxed1 | 19 | Master's Degree (Example: MA, MS, MEng, MEd, MBA) | 45878298 | Master's degree (e.g., MA, MS, MEng, MEd, MSW, MBA) | Meas Value | exactMatch 1 |
| 1492 | pxji1 | 2 | Fairly likely | 1989775 | Somewhat likely | Meas Value | closeMatch 1 |
| 1493 | pxji1 | 3 | Not too likely | 1990595 | Somewhat unlikely | Meas Value | closeMatch 1 |
| 1494 | pxji1 | 4 | Not at all likely | 45877240 | Very unlikely | Meas Value | closeMatch 1 |
| 1501 | pxji2 | 3 | Not easy at all | 45884578 | Very difficult | Meas Value | closeMatch 1 |
| 1535 | pxhic1 | 0 | Not Covered | 45881114 | Not Covered by Insurance | Meas Value | exactMatch 1 |
| 1539 | pxhic2 | 0 | Not Covered | 45881114 | Not Covered by Insurance | Meas Value | exactMatch 1 |
| 1543 | pxhic3 | 0 | Not Covered | 45881114 | Not Covered by Insurance | Meas Value | exactMatch 1 |
| 1547 | pxhic4 | 0 | Not Covered | 45881114 | Not Covered by Insurance | Meas Value | exactMatch 1 |
| 1551 | pxhic5 | 0 | Not Covered | 45881114 | Not Covered by Insurance | Meas Value | exactMatch 1 |
| 1555 | pxhic7 | 0 | Not Covered | 45881114 | Not Covered by Insurance | Meas Value | exactMatch 1 |
| 1562 | pxahc1 | 1 | Within the past year (anytime less than 12 months ago) | 45876704 | Within the past 12 months | Meas Value | exactMatch 1 |
| 1563 | pxahc1 | 2 | Within the last 2 years (1 year but less than 2 years ago) | 45876577 | More than 1 year, but not more than 2 years ago | Meas Value | exactMatch 1 |
| 1564 | pxahc1 | 3 | Within the last 3 years (2 years but less than 3 years ago) | 45876578 | More than 2 years, but not more than 3 years ago | Meas Value | exactMatch 1 |
| 1565 | pxahc1 | 4 | Within the last 5 years (3 years but less than 5 years ago) | 45880702 | More than 3 years, but not more than 5 years ago | Meas Value | exactMatch 1 |
| 1567 | pxahc1 | 6 | 10 years ago or more | 45881663 | 10 years or more | Meas Value | closeMatch 0.75 |
| 1575 | pxahc3 | 1 | Within the past year (anytime less than 12 months ago) | 45876704 | Within the past 12 months | Meas Value | exactMatch 1 |
| 1576 | pxahc3 | 2 | Within the last 2 years (1 year but less than 2 years ago) | 45876577 | More than 1 year, but not more than 2 years ago | Meas Value | exactMatch 1 |
| 1577 | pxahc3 | 3 | Within the last 3 years (2 years but less than 3 years ago) | 45876578 | More than 2 years, but not more than 3 years ago | Meas Value | exactMatch 1 |
| 1578 | pxahc3 | 4 | Within the last 5 years (3 years but less than 5 years ago) | 45880702 | More than 3 years, but not more than 5 years ago | Meas Value | exactMatch 1 |
| 1580 | pxahc3 | 6 | 10 years ago or more | 45881663 | 10 years or more | Meas Value | closeMatch 0.75 |
| 1592 | pxahc5 | 5 | Some other place | 45878142 | Other | Meas Value | closeMatch 1 |
| 1678 | cmroute | 8 | Inhalation | 40486069 | Respiratory tract | Route | closeMatch 1 |
| 1690 | cmdosu | 1 | Percent Volume per Volume | 45891010 | volume percent volume | Unit | exactMatch 1 |
| 1692 | cmdosu | 2 | Capsule | 32912 | Generic unit for indivisible thing | Unit | closeMatch 0.75 |
| 1696 | cmdosu | 4 | Inhalation | 45744809 | Actuation | Unit | closeMatch 1 |
| 1698 | cmdosu | 5 | International Dosing Unit | 8718 | international unit | Unit | closeMatch 0.75 |
| 1714 | cmdosu | 13 | Puff | 45744809 | Actuation | Unit | closeMatch 1 |
| 1751 | cmdosu | 14 | Spray | 45744809 | Actuation | Unit | closeMatch 1 |
| 1758 | cmdosfrq | QD | Daily | 45885250 | 1 time per day | Meas Value | exactMatch 1 |
| 1759 | cmdosfrq | BID | Twice Daily | 45883167 | 2 times per day | Meas Value | exactMatch 1 |
| 1760 | cmdosfrq | TID | Three Times Daily | 45883169 | 3 times per day | Meas Value | exactMatch 1 |
| 1761 | cmdosfrq | QID | Four times daily | 45882529 | 4 times per day | Meas Value | exactMatch 1 |
| 1859 | cmtrt_a1c | 1 | Yes | 4016042 | Diabetic on oral treatment | Observation | exactMatch 1 |
| 1863 | mhterm_dm2 | 1 | Yes | 201826 | Type 2 diabetes mellitus | Condition | exactMatch 1 |
| 1867 | mhterm_dm1 | 1 | Yes | 201254 | Type 1 diabetes mellitus | Condition | exactMatch 1 |
| 1868 | mhterm_predm | 1 | Yes | 37018196 | Prediabetes | Condition | exactMatch 1 |
| 1869 | mh_a1c | 1 | Yes | 4214376 | Hyperglycemia | Condition | closeMatch 0.75 |
| 1871 | cmtrt_insln | 1 | Yes | 440922 | Diabetic on insulin | Observation | closeMatch 0.75 |
| 1872 | cmtrt_glcs | 1 | Yes | 36714369 | Diabetic on non-insulin injectable medication | Observation | exactMatch 1 |
| 1912 | susmkncf | 1 | Yes | 40766306 | Smoked at least 100 cigarettes in entire life | Observation | exactMatch 1 |
| 1915 | susmkstaage | 98 | More than 60 years old | 45882614 | 60 or older | Meas Value | exactMatch 1 |
| 1917 | susmkcdur | 1 | Yes | 40766945 | Current smoker | Observation | exactMatch 1 |
| 1920 | susmkstoage | 98 | More than 60 years old | 45882614 | 60 or older | Meas Value | exactMatch 1 |
| 1922 | susmkdosfr | 21 | 21-30 (up to 1.5 packs) | 45881687 | 21-30 (2 points) | Meas Value | closeMatch 1 |
| 1930 | sualcage | 98 | More than 60 years old | 45882614 | 60 or older | Meas Value | exactMatch 1 |
| 1932 | suvptoyr | 98 | More than 60 years old | 45882614 | 60 or older | Meas Value | exactMatch 1 |
| 1937 | subrdosfr | 0 | Less than 1 | 45882032 | Less than 1 drink a week | Meas Value | exactMatch 1 |
| 1945 | suwndosfr | 0 | Less than 1 | 45882032 | Less than 1 drink a week | Meas Value | exactMatch 1 |
| 1954 | sulqdosfr | 0 | Less than 1 | 45882032 | Less than 1 drink a week | Meas Value | exactMatch 1 |
| 1968 | suvpstage | 98 | More than 60 years old | 45882614 | 60 or older | Meas Value | exactMatch 1 |
| 1970 | suvpcdur | 1 | Yes | 903655 | Electronic cigarette smoker | Observation | exactMatch 1 |
| 1974 | rp_childpot | 1 | Yes | 45884583 | Currently pregnant | Meas Value | exactMatch 1 |
| 1982 | sumrjstage | 98 | More than 60 years old | 45882614 | 60 or older | Meas Value | exactMatch 1 |
| 1984 | sumrjcdur | 1 | Yes | 37116660 | Marijuana user | Observation | exactMatch 1 |
| 1987 | sumrjtrt | 1 | Inhaled/Smoked (for example: joints, blunts, bongs, vaping, dabs, ) | 45877637 | Inhalation, respiratory | Meas Value | exactMatch 1 |
| 1988 | sumrjtrt | 2 | Oral/Edibles (for example: oils, tinctures, beverages, capsules, sprays) | 45878097 | Oral | Meas Value | exactMatch 1 |
| 1989 | sumrjtrt | 3 | Topical (for example: sprays or oils) | 45877645 | Topical | Meas Value | exactMatch 1 |
| 2081 | rtop_odd | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2082 | rtop_odm | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2083 | rtei_odir | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | closeMatch 0.75 |
| 2084 | rtei_odfaf | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | closeMatch 0.75 |
| 2085 | rtsm_odc | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2086 | rtsm_odn | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2087 | rtsm_odt | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2088 | rtsm_odm | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2089 | rtso_odo | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | closeMatch 1 |
| 2090 | rtso_odp | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | exactMatch 1 |
| 2091 | rtso_odm | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 1 |
| 2092 | rtci_odm1 | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | exactMatch 1 |
| 2093 | rtci_odd1 | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | closeMatch 1 |
| 2094 | rtci_odm2 | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 1 |
| 2095 | rtci_odd2 | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 0.75 |
| 2096 | rtma_odw | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | exactMatch 1 |
| 2097 | rtma_odm | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | exactMatch 1 |
| 2098 | rtma_odm1 | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 1 |
| 2099 | rttr_odr | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | exactMatch 1 |
| 2100 | rttr_odm1 | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 1 |
| 2101 | rttr_odm2 | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 1 |
| 2102 | rtfl_od | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | closeMatch 0.75 |
| 2103 | rtop_osd | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2104 | rtop_osm | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2105 | rtei_osir | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | closeMatch 0.75 |
| 2106 | rtei_osfaf | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | closeMatch 0.75 |
| 2107 | rtsm_osc | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2108 | rtsm_osn | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2109 | rtsm_ost | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2110 | rtsm_osm | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | exactMatch 1 |
| 2111 | rtso_oso | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | closeMatch 1 |
| 2112 | rtso_osp | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | exactMatch 1 |
| 2113 | rtso_osm | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 1 |
| 2114 | rtci_osm1 | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | exactMatch 1 |
| 2115 | rtci_osd1 | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | closeMatch 1 |
| 2116 | rtci_osm2 | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 1 |
| 2117 | rtci_osd2 | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 0.75 |
| 2118 | rtma_osw | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | exactMatch 1 |
| 2119 | rtma_osm | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | exactMatch 1 |
| 2120 | rtma_osm1 | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 1 |
| 2121 | rttr_osr | 1 | Yes | 1073298 | Optical coherence tomography of posterior segment of eye | Procedure | exactMatch 1 |
| 2122 | rttr_osm1 | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 1 |
| 2123 | rttr_osm2 | 1 | Yes | 745759 | Computerized ophthalmic diagnostic imaging (eg, optical coherence tomography [OC | Procedure | closeMatch 1 |
| 2124 | rtfl_os | 1 | Yes | 4063911 | Ocular fundus photography | Procedure | closeMatch 0.75 |
| 2129 | cmdosu | 19 | Milligram per Gram (mg/g) | 8723 | milligram per gram | Unit | exactMatch 1 |
| 2130 | cmdosu | 20 | Milligram per Milliliter (mg/mL) | 8861 | milligram per milliliter | Unit | exactMatch 1 |
| 2143 | rp_childpot | 0 | No | 42530854 | Not pregnant | Meas Value | exactMatch 1 |

## B2 Questions mapped to standard concepts (review each): 209
| Line | SRC_CODE | Source text | Concept | Target name | Domain | Predicate |
|---|---|---|---|---|---|---|
| 2 | viaocmpdat | Date BCVA performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 4 | viaodsph | OD - Autorefractor - Sphere | 3000744 | Right eye Sphere Autorefractor.auto | Measurement | closeMatch 1 |
| 5 | viaodcyl | OD - Autorefractor - Cylinder | 3033346 | Right eye Cylinder Autorefractor.auto | Measurement | closeMatch 1 |
| 6 | viaodaxi | OD - Autorefractor - Axis | 3034190 | Right eye Axis Autorefractor.auto | Measurement | closeMatch 1 |
| 7 | viaossph | OS - Autorefractor - Sphere | 3003500 | Left eye Sphere Autorefractor.auto | Measurement | closeMatch 1 |
| 8 | viaoscyl | OS - Autorefractor - Cylinder | 3002343 | Left eye Cylinder Autorefractor.auto | Measurement | closeMatch 1 |
| 9 | rp_childpot | Are you currently pregnant? | 40768856 | Are you currently pregnant [PhenX] | Observation | exactMatch 1 |
| 10 | viaosaxi | OS - Autorefractor - Axis | 3001254 | Left eye Axis Autorefractor.auto | Measurement | closeMatch 1 |
| 19 | scrsex | What sex were you assigned at birth? That is, what is on your original birth certificate? | 46235213 | Sex assigned at birth | Observation | closeMatch 1 |
| 20 | scrsexot | Other (please specify) | 46235213 | Sex assigned at birth | Observation | closeMatch 0.75 |
| 21 | ethnic | Are you of Hispanic, Latina/x or Spanish origin? Please check all that apply. | 42868351 | Hispanic, latino-a, or spanish origin | Observation | exactMatch 1 |
| 22 | ethnicot | Other (please specify) | 42868351 | Hispanic, latino-a, or spanish origin | Observation | closeMatch 0.75 |
| 24 | race | How would you describe your race/ethnicity? (check all that apply) | 3050381 | Race or ethnicity | Observation | closeMatch 1 |
| 25 | raceot | Other (please describe) | 3050381 | Race or ethnicity | Observation | closeMatch 0.75 |
| 26 | racetrib | Tribal affiliation (please describe) | 36660477 | Tribal affiliation | Observation | closeMatch 1 |
| 27 | race2 | Which one of these groups would you say best represents your race? | 3046853 | Race | Observation | closeMatch 1 |
| 45 | cl_maristatot | Other (please specify) | 4053609 | Marital status | Observation | closeMatch 0.75 |
| 46 | cesmpdat | CES-D-10 survey date | 4160030 | Performed | Observation | closeMatch 0.75 |
| 47 | ces1 | I was bothered by things that usually don't bother me | 1761605 | Bothered by things that are not usually bothersome | Observation | exactMatch 1 |
| 48 | ces2 | I had trouble keeping my mind on what I was doing | 1761791 | Trouble focusing | Observation | exactMatch 1 |
| 49 | ces3 | I felt depressed | 1761895 | Feeling depressed | Observation | exactMatch 1 |
| 50 | ces4 | I felt that everything I did was an effort | 1761503 | Feeling everything is too much of an effort | Observation | exactMatch 1 |
| 51 | ces5 | I felt hopeful about the future | 1761675 | Feeling hopeful about the future | Observation | exactMatch 1 |
| 52 | ces6 | I felt fearful | 1761739 | Feeling fearful | Observation | exactMatch 1 |
| 53 | ces7 | My sleep was restless | 1761695 | Restless sleep | Observation | exactMatch 1 |
| 54 | ces8 | I was happy | 1761700 | Feeling happy | Observation | exactMatch 1 |
| 55 | ces9 | I felt lonely | 1761319 | Feeling lonely | Observation | exactMatch 1 |
| 56 | ces10 | I could not "get going" | 1761073 | Lack of energy | Observation | exactMatch 1 |
| 57 | cestl | CESD-10 Score | 1761347 | Total Score CES-D | Observation | exactMatch 1 |
| 103 | icf_dat | Consent survey/form date (date survey/form opened) | 4160030 | Performed | Observation | closeMatch 0.75 |
| 104 | c184390 | Paper consent obtained | 3018196 | Informed consent obtained | Observation | closeMatch 1 |
| 105 | c184390_dat | Date paper consent completed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 108 | dmgcmpdat | Demographic survey date (date survey/form opened) | 4160030 | Performed | Observation | closeMatch 0.75 |
| 110 | cage | Age (in years) | 3022304 | Age | Observation | exactMatch 1 |
| 111 | cl_maristat | Marital Status | 4053609 | Marital status | Observation | exactMatch 1 |
| 122 | dvamwstdat | Date device given to participant | 4260905 | Date | Observation | exactMatch 1 |
| 123 | dvcgmstdat | Date sensor inserted | 4260905 | Date | Observation | exactMatch 1 |
| 124 | dvenvstdat | Date device given to participant | 4260905 | Date | Observation | exactMatch 1 |
| 126 | dvamwendat | Date device received back from participant | 4260905 | Date | Observation | exactMatch 1 |
| 128 | dvcgmendat | Date device received back from participant | 4260905 | Date | Observation | exactMatch 1 |
| 130 | dvenvendat | Date device received back from participant | 4260905 | Date | Observation | exactMatch 1 |
| 136 | dvamwendhand | Participant's dominant hand | 40768726 | Dominant hand [PhenX] | Observation | exactMatch 1 |
| 141 | dmlcmpdat | Diabetes survey date | 4160030 | Performed | Observation | closeMatch 0.75 |
| 143 | dmlact | What would you consider your typical activity level to be? | 44808782 | Level of physical activity | Observation | closeMatch 1 |
| 147 | dmlpor | When reflecting on your typical eating habits, which of the following best describes your approach t | 764035 | Able to control portion size | Observation | closeMatch 0.75 |
| 148 | dmlfrveg | In a typical day, how many servings of fruits and vegetables do you consume? | 4295005 | Number of portions of fruit and vegetables daily | Observation | closeMatch 0.75 |
| 194 | dietcmpdat | Dietary survey date | 4160030 | Performed | Observation | closeMatch 0.75 |
| 196 | diet1 | How many times a week did you eat fast food meals or snacks? | 40771095 | How many times a week did you eat fast food or snacks or pizza in past 7 days [S | Observation | exactMatch 1 |
| 197 | diet2 | How many servings of fruit did you eat each day? | 21493059 | Fruit servings 24 hour Estimated | Observation | exactMatch 1 |
| 199 | diet3 | How many servings of vegetables did you eat each day? | 21493061 | Vegetable servings 24 hour Estimated | Observation | exactMatch 1 |
| 200 | diet4 | How many regular sodas or glasses of sweet tea did you drink each day? | 37311745 | Estimated oral intake of sugar sweetened drinks in 24 hours | Observation | closeMatch 0.75 |
| 246 | eos_dsdecod | What was the primary reason the subject discontinued? | 44810920 | Withdrawn from research study | Observation | relatedMatch 0.5 |
| 247 | eos_dsstdat | What was the study discontinuation or completion date? | 4260905 | Date | Observation | exactMatch 1 |
| 248 | eos_dsdecodie | Mark questions from Inclusion/Exclusion that were not met. | 44811374 | Not eligible for participation in research study | Observation | relatedMatch 0.75 |
| 268 | dricmpdat | Date driving record assessment conducted | 4260905 | Date | Observation | exactMatch 1 |
| 279 | rtfncmpdattim | Date & time Fundus - Edion performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 280 | rtfnocmpdattim | Date & time Fundus - Optomed performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 281 | rthracmpdattim | Date & time OCT & OCTA - Spectralis HRA OCT performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 282 | rtoctcmpdattim | Date & time OCT - Triton OCT performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 283 | rtm2cmpdattim | Date & time OCT & OCTA - Maestro2 performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 284 | rtfliocmpdattim | Date & time FLIO performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 285 | rtaccmpdattim | Date & time Angioplex - Cirrus 5000 performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 286 | rtekgcmpdattim | Date & time Cardiology - EKG - Pagewriter TC30 Cardiograp performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 287 | faqcmpdat | FAQ Survey date (date survey/form opened) | 4160030 | Performed | Observation | closeMatch 0.75 |
| 290 | mhcmpdat | Health survey date | 4160030 | Performed | Observation | closeMatch 0.75 |
| 324 | mhoccur_fall | Have you fallen in the last 12 months? (a fall is defined as an event which results in a person comi | 40757198 | Falls in the past year | Observation | closeMatch 1 |
| 325 | mhoccur_fallot | If so, how many times in the last 12 months? | 4310026 | Number of falls in last year | Observation | closeMatch 1 |
| 332 | cmdos | Amount taken (Dose) | 4162374 | Drug dose | Observation | closeMatch 1 |
| 334 | cmdosfrq | Frequency taken or applied: | 3042548 | Current medication, Frequency | Observation | closeMatch 1 |
| 442 | exportzip | Zip Code for Export | 3043579 | Postal code [Location] | Observation | closeMatch 1 |
| 505 | 33762-6 | Natriuretic peptide.B prohormone N-Terminal [Mass/volume] in Serum or Plasma | 3029187 | Natriuretic peptide.B prohormone N-Terminal [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 509 | 67151-1 | Troponin T.cardiac [Mass/volume] in Serum or Plasma by High sensitivity method | 40769783 | Troponin T.cardiac [Mass/volume] in Serum or Plasma by High sensitivity method | Measurement | exactMatch 1 |
| 513 | 1986-9 | C peptide [Mass/volume] in Serum or Plasma | 3010084 | C peptide [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 517 | 3695-4 | Insulin [Mass/volume] in Serum or Plasma | 3022466 | Insulin [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 524 | 30522-7 | C reactive protein [Mass/volume] in Serum or Plasma by High sensitivity method | 3010156 | C reactive protein [Mass/volume] in Serum or Plasma by High sensitivity method | Measurement | exactMatch 1 |
| 528 | 2093-3 | Cholesterol [Mass/volume] in Serum or Plasma | 3027114 | Cholesterol [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 531 | 2571-8 | Triglyceride [Mass/volume] in Serum or Plasma | 3022192 | Triglyceride [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 534 | 2085-9 | Cholesterol in HDL [Mass/volume] in Serum or Plasma | 3007070 | Cholesterol in HDL [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 537 | 13457-7 | Cholesterol in LDL [Mass/volume] in Serum or Plasma by calculation | 3028288 | Cholesterol in LDL [Mass/volume] in Serum or Plasma by calculation | Measurement | exactMatch 1 |
| 540 | 2345-7 | Glucose [Mass/volume] in Serum or Plasma | 3004501 | Glucose [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 544 | 3094-0 | Urea nitrogen [Mass/volume] in Serum or Plasma | 3013682 | Urea nitrogen [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 548 | 2160-0 | Creatinine [Mass/volume] in Serum or Plasma | 3016723 | Creatinine [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 554 | 31045-8 | BUN/Creatinine ratio | 3033837 | Creatinine/Urea nitrogen [Mass Ratio] in Serum or Plasma | Measurement | exactMatch 1 |
| 555 | 2951-2 | Sodium [Moles/volume] in Serum or Plasma | 3019550 | Sodium [Moles/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 559 | 2823-3 | Potassium [Moles/volume] in Serum or Plasma | 3023103 | Potassium [Moles/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 563 | 2075-0 | Chloride [Moles/volume] in Serum or Plasma | 3014576 | Chloride [Moles/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 567 | 2028-9 | Carbon dioxide, total [Moles/volume] in Serum or Plasma | 3015632 | Carbon dioxide, total [Moles/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 571 | 17861-6 | Calcium [Mass/volume] in Serum or Plasma | 3006906 | Calcium [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 575 | 2885-2 | Protein [Mass/volume] in Serum or Plasma | 3020630 | Protein [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 579 | 1751-7 | Albumin [Mass/volume] in Serum or Plasma | 3024561 | Albumin [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 583 | 2336-6 | Globulin [Mass/volume] in Serum | 3021886 | Globulin [Mass/volume] in Serum | Measurement | exactMatch 1 |
| 584 | 1759-0 | Albumin/Globulin ratio | 3020509 | Albumin/Globulin [Mass Ratio] in Serum or Plasma | Measurement | exactMatch 1 |
| 585 | 1975-2 | Bilirubin.total [Mass/volume] in Serum or Plasma | 3024128 | Bilirubin.total [Mass/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 586 | 6768-6 | Alkaline phosphatase [Enzymatic activity/volume] in Serum or Plasma | 3035995 | Alkaline phosphatase [Enzymatic activity/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 592 | 1920-8 | Aspartate aminotransferase [Enzymatic activity/volume] in Serum or Plasma | 3013721 | Aspartate aminotransferase [Enzymatic activity/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 596 | 1742-6 | Alanine aminotransferase [Enzymatic activity/volume] in Serum or Plasma | 3006923 | Alanine aminotransferase [Enzymatic activity/volume] in Serum or Plasma | Measurement | exactMatch 1 |
| 603 | 4548-4 | Hemoglobin A1c/Hemoglobin.total in Blood | 3004410 | Hemoglobin A1c/Hemoglobin.total in Blood | Measurement | exactMatch 1 |
| 610 | 2161-8 | Creatinine [Mass/volume] in Urine | 3017250 | Creatinine [Mass/volume] in Urine | Measurement | exactMatch 1 |
| 612 | 1754-1 | Albumin [Mass/volume] in Urine | 3012516 | Albumin [Mass/volume] in Urine | Measurement | exactMatch 1 |
| 614 |  | MOCA Date | 3006440 | Date form completed | Observation | exactMatch 1 |
| 643 | years_of_education | Years of Education | 42528764 | Years of education [#] - Reported | Observation | exactMatch 1 |
| 645 | moca_total_score_time | Total Score (Time) | 1988422 | Time to complete survey | Observation | closeMatch 0.75 |
| 647 | moca_total_score | Total Score | 606671 | Montreal Cognitive Assessment version 8.1 | Measurement | exactMatch 1 |
| 671 | lbdattim1 | Date & time clinical labs performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 672 | lbscat_wbc | White Blood Cells (WBC) - x10E3/µL | 3000905 | Leukocytes [#/volume] in Blood by Automated count | Measurement | exactMatch 1 |
| 673 | lbscat_rbc | Red Blood Cells (RBC) - x10E6/µL | 3020416 | Erythrocytes [#/volume] in Blood by Automated count | Measurement | exactMatch 1 |
| 674 | lbscat_a1c | Hemoglobin - g/dL | 3000963 | Hemoglobin [Mass/volume] in Blood | Measurement | exactMatch 1 |
| 675 | lbscat_hct | Hematocrit - % | 3023314 | Hematocrit [Volume Fraction] of Blood by Automated count | Measurement | exactMatch 1 |
| 676 | lbscat_mcv | MCV - fL | 3023599 | MCV [Entitic mean volume] in Red Blood Cells by Automated count | Measurement | exactMatch 1 |
| 677 | lbscat_mch | MCH - pg | 3012030 | MCH [Entitic mass] by Automated count | Measurement | exactMatch 1 |
| 678 | lbscat_mchc | MCHC - g/dL | 3009744 | MCHC [Entitic Mass/volume] in Red Blood Cells by Automated count | Measurement | exactMatch 1 |
| 679 | lbscat_rdw | RDW - % | 3019897 | Erythrocyte [DistWidth] in Red Blood Cells by Automated count | Measurement | exactMatch 1 |
| 680 | lbscat_plt | Platelets - x10E3/µL | 3024929 | Platelets [#/volume] in Blood by Automated count | Measurement | exactMatch 1 |
| 681 | cmcmpdat | Date medications assessment conducted | 4260905 | Date | Observation | exactMatch 1 |
| 732 | mlcscmpdat | Date procedure performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 739 | mocacmpdattim | Date time MoCA performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 741 | msscmpdat | Date monofilament performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 742 | mssrf1 | Site 1 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 743 | mssrf2 | Site 2 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 744 | mssrf3 | Site 3 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 745 | mssrf4 | Site 4 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 746 | mssrf5 | Site 5 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 747 | mssrf6 | Site 6 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 748 | mssrf7 | Site 7 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 749 | mssrf8 | Site 8 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 750 | mssrf9 | Site 9 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 751 | mssrf10 | Site 10 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 754 | msslf1 | Site 1 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 755 | msslf2 | Site 2 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 756 | msslf3 | Site 3 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 757 | msslf4 | Site 4 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 758 | msslf5 | Site 5 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 759 | msslf6 | Site 6 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 760 | msslf7 | Site 7 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 761 | msslf8 | Site 8 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 762 | msslf9 | Site 9 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 763 | msslf10 | Site 10 | 4047085 | Monofilament foot sensation test | Procedure | exactMatch 1 |
| 766 | viacmpdat | Ophthalmic survey date | 4160030 | Performed | Observation | closeMatch 0.75 |
| 769 | via3 | Because of your eyesight, how much difficulty do you have noticing objects off to the side while you | 40768765 | Level of difficulty seeing objects off to the side | Observation | closeMatch 0.75 |
| 770 | via4 | When was the last time you had your eyes examined by an eye care provider (ophthalmologist or optome | 40758529 | Date of last eye examination | Observation | closeMatch 0.75 |
| 812 | paidcmpdat | PAID-5 DM survey date | 4160030 | Performed | Observation | closeMatch 0.75 |
| 846 | prtcmpdat | Participant contact survey/form date (date survey/form opened) | 4160030 | Performed | Observation | closeMatch 0.75 |
| 847 | plcscmpdat | Date procedure performed | 4160030 | Performed | Observation | closeMatch 0.75 |
| 854 | pacmpdat | Date Assessment Performed --- Populated if an in person visit was completed (regardless of the physi | 4160030 | Performed | Observation | closeMatch 0.75 |
| 856 | height_vsorres | Height (cm) | 3036277 | Body height | Measurement | exactMatch 1 |
| 857 | weight_vsorres | Weight (kilograms) | 3025315 | Body weight | Measurement | exactMatch 1 |
| 858 | bmi_vsorres | BMI | 3038553 | Body mass index (BMI) [Ratio] | Measurement | exactMatch 1 |
| 859 | waist_vsorres | Waist Circumference (cm) | 3016258 | Waist Circumference at umbilicus by Tape measure | Measurement | closeMatch 1 |
| 860 | hip_vsorres | Hip Circumference (cm) | 4111665 | Hip circumference | Measurement | exactMatch 1 |
| 861 | whr_vsorres | Waist to Hip Ratio (WHR) | 4087501 | Waist/hip ratio | Measurement | exactMatch 1 |
| 862 | bp1_sysbp_vsorres | Systolic (mmHg) | 3004249 | Systolic blood pressure | Measurement | exactMatch 1 |
| 863 | bp1_diabp_vsorres | Diastolic (mmHg) | 3012888 | Diastolic blood pressure | Measurement | exactMatch 1 |
| 864 | pulse_vsorres | Heart Rate (bpm) | 3027018 | Heart rate | Measurement | exactMatch 1 |
| 865 | bp2_sysbp_vsorres | Systolic (mmHg) | 3004249 | Systolic blood pressure | Measurement | exactMatch 1 |
| 866 | bp2_diabp_vsorres | Diastolic (mmHg) | 3012888 | Diastolic blood pressure | Measurement | exactMatch 1 |
| 867 | pulse_vsorres_2 | Heart Rate (bpm) | 3027018 | Heart rate | Measurement | exactMatch 1 |
| 873 | preconcmpdat | Pre-consent survey/form date (date survey/form opened) | 4160030 | Performed | Observation | closeMatch 0.75 |
| 876 | pxsficmpdat | PhenX Food Insecurity survey date | 4160030 | Performed | Observation | closeMatch 0.75 |
| 877 | pxfi1 | The first statement is, "The food that (I/we) bought just didn't last, and (I/we) didn't have money  | 36306143 | Within the past 12 months the food we bought just didn't last and we didn't have | Observation | exactMatch 1 |
| 878 | pxfi2 | "(I/we) couldn't afford to eat balanced meals." Was that often, sometimes, or never true for (you/yo | 36660487 | In the last 12 months, we couldn't afford to eat balanced meals [U.S. FSS] | Observation | exactMatch 1 |
| 879 | pxfi3 | In the last year, did you and/or other adults in your household ever cut the size of your meals or s | 36660433 | In the last 12 months, did you ever cut the size of your meals or skip meals bec | Observation | exactMatch 1 |
| 880 | food_insecurity_change_diet_frequency | How often did this happen - almost every month, some months but not every month, or in only 1 or 2 m | 36660018 | In the last 12 months, how often did you cut the size of your meals or skip meal | Observation | closeMatch 1 |
| 881 | pxfi4 | In the last 12 months, did you ever eat less than you felt you should because there wasn't enough mo | 36659800 | In the last 12 months, did you ever eat less than you felt you should because th | Observation | exactMatch 1 |
| 882 | pxfi5 | In the last 12 months, were you ever hungry but didn't eat because you couldn't afford enough food? | 36660509 | In the last 12 months, were you ever hungry but didn't eat because there wasn't  | Observation | exactMatch 1 |
| 913 | pxnecmpdat | PhenX Neighborhood Enviroment survey date | 4160030 | Performed | Observation | closeMatch 0.75 |
| 914 | pxne1 | What is the main type of housing in your neighborhood? | 40769029 | What is the main type of housing in your neighborhood [PhenX] | Observation | exactMatch 1 |
| 915 | pxne2 | Many shops, stores, markets or other places to buy things I need are within easy walking distance of | 40769030 | Many shops, stores, markets, or other places to buy things I need are within eas | Observation | exactMatch 1 |
| 916 | pxne3 | It is within a 10-15 minute walk to a transit stop (such as bus, train, trolley, or tram) from my ho | 40769031 | It is within a 10-15 minute walk to a transit stop, such as bus, train, trolley, | Observation | exactMatch 1 |
| 917 | pxne4 | There are sidewalks on most of the streets in my neighborhood. Would you say that you... | 40769032 | There are sidewalks on most of the streets in my neighborhood [PhenX] | Observation | exactMatch 1 |
| 918 | pxne5 | There are facilities to bicycle in or near my neighborhood, such as special lanes, separate paths or | 40769033 | There are facilities to bicycle in or near my neighborhood, such as special lane | Observation | exactMatch 1 |
| 919 | pxne6 | My neighborhood has several free or low cost recreation facilities, such as parks, walking trails, b | 40769034 | My neighborhood has several free or low-cost recreation facilities, such as park | Observation | exactMatch 1 |
| 920 | pxne7 | The crime rate in my neighborhood makes it unsafe to go on walks at night. Would you say that you... | 40769035 | The crime rate in my neighborhood makes it unsafe to go on walks at night [PhenX | Observation | exactMatch 1 |
| 929 | pxne16 | The crime rate in my neighborhood makes it unsafe to go on walks during the day. Would you say that  | 40192414 | The crime rate in my neighborhood makes it unsafe to go on walks during the day. | Observation | exactMatch 1 |
| 1043 | pxrdcmpdat | PhenX Racial/Ethnic Discrimination survey date | 4160030 | Performed | Observation | closeMatch 0.75 |
| 1407 | pxsdohcmpdat | PhenX SDOH survey date | 4160030 | Performed | Observation | closeMatch 0.75 |
| 1409 | pxep1 | Is English your first language? | 40757199 | Language.primary is English | Observation | closeMatch 0.75 |
| 1411 | pxep3 | Since you speak a language other than English at home, we are interested in your own opinion of how  | 40769340 | How well do you speak English [NLAAS] | Observation | closeMatch 1 |
| 1412 | pxed1 | What is the highest grade or level of school you have completed or the highest degree you have recei | 40766232 | What is the highest grade or level of school you have completed or the highest d | Observation | closeMatch 1 |
| 1438 | pxdhc1 | You are treated with less courtesy than other people. | 40770200 | You have been treated with less courtesy than other people [PhenX] | Observation | closeMatch 0.75 |
| 1439 | pxdhc2 | You are treated with less respect than other people. | 40770201 | You have been treated with less respect than other people [PhenX] | Observation | closeMatch 0.75 |
| 1440 | pxdhc3 | You receive poorer service than others. | 40192503 | How often do you receive poorer service than others when you go to a doctor's of | Observation | closeMatch 0.75 |
| 1441 | pxdhc4 | A doctor or nurse acts as if he or she thinks you are not smart. | 40192505 | How often does a doctor or nurse act as if he or she thinks you are not smart wh | Observation | closeMatch 0.75 |
| 1442 | pxdhc5 | A doctor or nurse acts as if he or she is afraid of you. | 40192423 | How often does a doctor or nurse act as if he or she is afraid of you when you g | Observation | closeMatch 0.75 |
| 1443 | pxdhc6 | A doctor or nurse acts as if he or she is better than you. | 40192383 | How often does a doctor or nurse act as if he or she is better than you when you | Observation | closeMatch 0.75 |
| 1444 | pxdhc7 | You feel like a doctor or nurse is not listening to what you were saying | 40192394 | How often do you feel like a doctor or nurse is not listening to what you were s | Observation | closeMatch 0.75 |
| 1673 | reccmpdat | Recruitment survey date (date survey/form opened) | 4160030 | Performed | Observation | closeMatch 0.75 |
| 1715 | 32294-1 | Albumin/Creatinine [Ratio] in Urine | 3020682 | Albumin/Creatinine [Ratio] in Urine | Measurement | exactMatch 1 |
| 1742 | rt_dat | Assessment Date | 4260905 | Date | Observation | exactMatch 1 |
| 1847 | scrcmpdat | Screening survey date (date survey/form opened) | 4160030 | Performed | Observation | closeMatch 0.75 |
| 1851 | mh_dm_age | If yes, at what age were you first diagnosed? | 4307859 | Age at diagnosis | Observation | closeMatch 0.75 |
| 1879 | lbdattim2 | Date & Time Draw Performed | 40771497 | Collection date and time of Specimen | Observation | closeMatch 1 |
| 1880 | icfa_dat | Date of Consent Attestation | 4160030 | Performed | Observation | closeMatch 0.75 |
| 1881 | visdat | Planned date & time of in-person visit | 4260905 | Date | Observation | exactMatch 1 |
| 1882 | studyid | Participant Study ID | 42528934 | Participant identifier | Observation | exactMatch 1 |
| 1883 | sucmpdat | Substance use survey date | 4160030 | Performed | Observation | closeMatch 0.75 |
| 1884 | susmkncf | Have you smoked at least 100 cigarettes or more in your lifetime? (100 cigarettes = 5 packs) | 40766306 | Smoked at least 100 cigarettes in entire life | Observation | exactMatch 1 |
| 1885 | susmkstaage | At what age did you start smoking? (Age started - years old) | 40770348 | At which age did you start smoking [PhenX] | Observation | exactMatch 1 |
| 1886 | susmkcdur | Do you smoke now? | 40766945 | Current smoker | Observation | exactMatch 1 |
| 1887 | susmkstoage | How many total years have you smoked? | 40770349 | Smoking tobacco use duration | Observation | exactMatch 1 |
| 1888 | susmkdosfr | On average how many cigarettes do/did you usually smoke in a day? (Number of cigarettes \| 20 cigaret | 40769208 | How many of these do you smoke per day [#] [PhenX] | Observation | closeMatch 1 |
| 1889 | sualckncf | Have you ever consumed alcohol? | 40772145 | Do you ever drink alcohol - including beer or wine [Reported.PHQ] | Observation | closeMatch 0.75 |
| 1890 | sualcage | At what age did you start drinking alcohol? (Age started - years old) | 40766301 | At what age did you begin to drink regularly - that is, drinking at least once a | Observation | closeMatch 0.75 |
| 1891 | suvptoyr | How many total years have you consumed alcohol? | 44786670 | Number of years alcohol consumed [Time] | Observation | closeMatch 0.75 |
| 1893 | subrdosfr | During the average week, how many 12 oz. bottles or cans of beer do you usually drink? (Number of bo | 40766674 | How many drinks per day, week, month, or year did you usually have [PhenX] | Observation | closeMatch 0.75 |
| 1905 | sumrjstage | At what age did you start using marijuana? (Age started - years old) | 37020592 | Age when first used marijuana | Observation | exactMatch 1 |
| 2125 | 3097-3 | BUN/Creatinine ratio | 3018311 | Urea nitrogen/Creatinine [Mass Ratio] in Serum or Plasma | Measurement | exactMatch 1 |
| 2127 | lbscat_nrbc | NRBC - % | 40761514 | Nucleated erythrocytes/Leukocytes [Ratio] in Blood by Automated count | Measurement | exactMatch 1 |
| 2139 | rtekgcmpdattim | Date & time Cardiology - EKG - Pagewriter TC30 Cardiograp performed | 4145308 | 12 lead ECG | Procedure | exactMatch 1 |
| 2140 | cmcmpdat2 | Date current medication collected | 4260905 | Date | Observation | exactMatch 1 |

## C1 'Other' rows and their predicates (should follow one convention): 17
| Line | Field | Source text | Concept | Target name | Predicate |
|---|---|---|---|---|---|
| 20 | scrsexot | Other (please specify) | 46235213 | Sex assigned at birth | closeMatch 0.75 |
| 22 | ethnicot | Other (please specify) | 42868351 | Hispanic, latino-a, or spanish origin | closeMatch 0.75 |
| 25 | raceot | Other (please describe) | 3050381 | Race or ethnicity | closeMatch 0.75 |
| 45 | cl_maristatot | Other (please specify) | 4053609 | Marital status | closeMatch 0.75 |
| 59 | mhcat_dmtaot | Other (please specify): | 2005200014 | Has a doctor or other healthcare professional ever | exactMatch 1 |
| 120 | cl_maristat=888 | Other | 45878142 | Other | exactMatch 1 |
| 259 | eos_dsdecod=888 | Other {eos_dsterm} | 45878142 | Other | exactMatch 1 |
| 264 | eos_dsdecodie=888 | Other | 45878142 | Other | exactMatch 1 |
| 292 | mhoccur_cvdot | Other heart issues (Examples: pacemaker, heart valve disease | 2005200014 | Has a doctor or other healthcare professional ever | exactMatch 1 |
| 303 | mhoccur_cns | Other neurological conditions | 2005200014 | Has a doctor or other healthcare professional ever | exactMatch 1 |
| 362 | mhcat_adot=888 | Other | 45878142 | Other | exactMatch 1 |
| 448 | scrsex=888 | Other | 45878142 | Other | exactMatch 1 |
| 458 | ethnic=888 | Yes, Other | 45878142 | Other | exactMatch 1 |
| 467 | race=888 | Other race, ethnicity or origin | 45878142 | Other | exactMatch 1 |
| 476 | race2=888 | Other race, ethnicity or origin | 45878142 | Other | exactMatch 1 |
| 804 | via5=7 | Other | 45878142 | Other | exactMatch 1 |
| 1766 | cmdosfrq=888 | Other | 45878142 | Other | exactMatch 1 |

## C2 Predicate / confidence combinations: 6
| Predicate | Confidence | Rows |
|---|---|---|
| skos:exactMatch | 1 | 1779 |
| skos:closeMatch | 1 | 170 |
| skos:closeMatch | 0.75 | 117 |
| (blank) | (blank) | 75 |
| skos:relatedMatch | 0.5 | 1 |
| skos:relatedMatch | 0.75 | 1 |

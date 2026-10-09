"""Two-way doors between every map."""
from content.maphelp import link

# ---- prologue -------------------------------------------------------------
link("desa_awal", "pantai_awal", (2, 20), (45, 18), size=(2, 4))
link("desa_awal", "prologue_festival", (24, 2), (20, 27), size=(3, 2))
link("desa_awal", "sumatra_desa", (45, 19), (2, 22), size=(2, 4))

# ---- sumatra --------------------------------------------------------------
link("sumatra_desa", "sumatra_hutan", (2, 20), (52, 20), size=(2, 4))
link("sumatra_desa", "sumatra_danau", (24, 2), (26, 37), size=(3, 2))
link("sumatra_desa", "java_desa", (46, 19), (2, 24), size=(2, 4))

# ---- java -----------------------------------------------------------------
link("java_desa", "java_sawah", (2, 24), (52, 20), size=(2, 4))
link("java_desa", "java_pasar", (46, 24), (2, 16), size=(2, 4))
link("java_desa", "java_candi", (24, 3), (24, 36), size=(3, 2))
link("java_pasar", "java_sawah", (42, 16), (4, 26), size=(2, 3))
link("java_pasar", "kalimantan_desa", (22, 32), (25, 8), size=(3, 2))

# ---- kalimantan -----------------------------------------------------------
link("kalimantan_desa", "kalimantan_sungai", (6, 20), (50, 34), size=(2, 4))
link("kalimantan_desa", "kalimantan_pasar", (28, 36), (14, 28), size=(3, 2))
link("kalimantan_desa", "kalimantan_hutan", (44, 28), (3, 18), size=(2, 4))
link("kalimantan_sungai", "kalimantan_hutan", (46, 34), (52, 34), size=(2, 4))

# ---- sulawesi -------------------------------------------------------------
link("kalimantan_pasar", "sulawesi_desa", (38, 22), (3, 24), size=(3, 3))
link("sulawesi_desa", "sulawesi_bukit", (24, 3), (24, 34), size=(3, 2))
link("sulawesi_desa", "sulawesi_pantai", (2, 22), (8, 30), size=(2, 3))
link("sulawesi_desa", "sulawesi_pelabuhan", (46, 22), (3, 26), size=(2, 4))

# ---- papua ----------------------------------------------------------------
link("sulawesi_pelabuhan", "papua_danau", (24, 9), (26, 36), size=(3, 2))
link("sulawesi_pantai", "papua_danau", (43, 20), (2, 28), size=(2, 3))
link("papua_danau", "papua_desa", (2, 30), (46, 20), size=(2, 4))
link("papua_desa", "papua_lembah", (2, 22), (52, 22), size=(2, 4))
link("papua_desa", "papua_hutan", (24, 3), (26, 36), size=(3, 2))

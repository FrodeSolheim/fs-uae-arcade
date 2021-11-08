title = "FS-UAE Arcade"
name = "fs-uae-arcade"
py_name = "fs_uae_arcade"
tar_name = "fs-uae-arcade"
version = "9.8.7dummy"
author = "Frode Solheim"
author_email = "frode@fs-uae.net"
package_map = {
    "arcade": ".",
    "fsbc": ".",
    "fsboot": ".",
    "fsgs": ".",
    "fspy": ".",
    "fstd": ".",
    "fsui": ".",
    "launcher": ".",
    "OpenGL": ".",
    "oyoyo": ".",
    "workspace": ".",
}
packages = sorted(package_map.keys())
scripts = ["fs-uae-arcade"]

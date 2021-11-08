title = "FS-UAE Arcade"
name = "fs-uae-arcade"
py_name = "fs_uae_arcade"
tar_name = "fs-uae-arcade"
version = "9.8.7dummy"
author = "Frode Solheim"
author_email = "frode@fs-uae.net"
package_map = {
    "arcade": "../fs-uae-launcher",
    "fsbc": "../fs-uae-launcher",
    "fsboot": "../fs-uae-launcher",
    "fsgs": "../fs-uae-launcher",
    "fspy": "../fs-uae-launcher",
    "fstd": "../fs-uae-launcher",
    "fsui": "../fs-uae-launcher",
    "launcher": "../fs-uae-launcher",
    "OpenGL": "../fs-uae-launcher",
    "oyoyo": "../fs-uae-launcher",
    "workspace": "../fs-uae-launcher",
}
packages = sorted(package_map.keys())
scripts = ["fs-uae-arcade"]

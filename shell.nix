{ pkgs ? import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/nixos-24.05.tar.gz";
  }) {}
}:

let
  python = pkgs.python310.withPackages (ps: with ps; [
    setuptools
  ]);
in
pkgs.mkShell {
  packages = [
    python
    pkgs.scons
    pkgs.ninja
    pkgs.pkg-config
    pkgs.gcc
    pkgs.mold-wrapped
    pkgs.glib
    pkgs.libpcap
    pkgs.boost
    pkgs.pixman
    pkgs.nlohmann_json
    pkgs.gperftools
    pkgs.git
    pkgs.autoconf
    pkgs.gnumake
    pkgs.gnum4
    pkgs.flex
    pkgs.bison
    pkgs.bc
    pkgs.elfutils
    pkgs.wget
    pkgs.vim
    pkgs.tmux
    pkgs.unzip
    pkgs.perl
    pkgs.rsync
    pkgs.verilator
    pkgs.which
  ];

  shellHook = ''
    if [ -f .envrc ]; then
      source .envrc
    fi
  '';
}

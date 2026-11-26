{
  description = "osu-native-py";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          dotnet-sdk_10
          clang
          zlib
          gnumake
          just
          python3
          poetry
        ];

        shellHook = ''
          echo "osu-native-py"
          echo "  just all        (native lib + bindings + install)"
          echo "  just test       (pytest)"
          echo "  just lint       (pre-commit)"
          echo "  just type-check (mypy)"
        '';
      };
    };
}

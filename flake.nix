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
          python3
          poetry
        ];

        shellHook = ''
          echo "osu-native-py"
          echo "  make all        (native lib + bindings + install)"
          echo "  make test       (pytest)"
          echo "  make lint       (pre-commit)"
          echo "  make type-check (mypy)"
        '';
      };
    };
}

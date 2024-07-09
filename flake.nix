{
  inputs.dev.url = "github:fmahnke/mkpkgs-dev";

  outputs = { self, nixpkgs, dev, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (pkgs) python3;

      buildInputs = with python3.pkgs; [ setuptools ];

      propagatedBuildInputs = with python3.pkgs; [
        # image processing
        numpy
        pillow
        # base
        tomlkit
      ];

      nativeBuildInputs = with pkgs;
        [
          # video processing
          ffmpeg
        ];
    in {
      packages.${system}.default = python3.pkgs.buildPythonPackage {
        version = "0.1.0";

        pname = "mortar";
        format = "pyproject";

        src = ./python-project;

        dontCheckRuntimeDeps = true;

        inherit propagatedBuildInputs buildInputs nativeBuildInputs;
      };

      hydraJobs = { inherit (self) packages; };

      devShells.${system} = {
        default = pkgs.mkShell {
          inputsFrom = [ dev.devShells.${system}.python ];

          packages = propagatedBuildInputs ++ nativeBuildInputs;
        };
      };
    };
}

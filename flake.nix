{
  inputs = {
    dev.url = "github:fmahnke/mkpkgs-dev";
    pymk.url = "github:fmahnke/pymk";
  };

  outputs = { self, nixpkgs, dev, pymk, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (pkgs) python3;

      buildInputs = with python3.pkgs; [ setuptools ];

      propagatedBuildInputs = with python3.pkgs; [
        ipython
        # image processing
        matplotlib
        numpy
        pillow
        types-pillow
        pyopengl
        opencv4
        # base
        pymk.packages.${system}.default
        tomlkit
      ];

      nativeBuildInputs = with pkgs;
        [
          pdm
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
          inputsFrom =
            [ dev.devShells.${system}.python dev.devShells.${system}.opengl ];

          packages = propagatedBuildInputs ++ nativeBuildInputs;
        };
      };
    };
}
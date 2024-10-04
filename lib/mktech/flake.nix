{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    dev.url = "github:fmahnke/mkpkgs-dev";
  };

  outputs = { self, nixpkgs, ... }@inputs:
    with inputs;
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pythonPkgs = pkgs.python3.pkgs;

      buildInputs = with pythonPkgs; [ tomlkit setuptools ];

    in {
      packages.x86_64-linux.default = pythonPkgs.buildPythonPackage {
        pname = "mktech";
        version = "0.1.0";
        pyproject = true;

        src = ./python;

        inherit buildInputs;

        nativeCheckInputs =
          [ inputs.dev.devShells.${system}.python.nativeBuildInputs ];

        checkPhase = ''
          nox
        '';
      };

      hydraJobs = { inherit (self) packages; };

      devShells.${system}.default = pkgs.mkShell {
        inputsFrom = [ inputs.dev.devShells.${system}.python ];

        inherit buildInputs;
      };
    };
}


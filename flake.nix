{
  description = "Rime - Universal Filename Sanitizer, Case Transformer & Batch Rename Engine";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    prism = {
      url = "github:SpanishSyntax/Prism";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    prism,
  }: let
    systems = flake-utils.lib.defaultSystems;
  in
    flake-utils.lib.eachSystem systems (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [prism.overlays.default];
      };
      lib = pkgs.lib;

      rimePackage = pkgs.python3Packages.buildPythonApplication {
        pname = "rime";
        version = "0.1.0";
        src = pkgs.lib.cleanSource ./.;
        pyproject = true;

        build-system = [
          pkgs.python3Packages.setuptools
        ];

        propagatedBuildInputs = [
          pkgs.python3Packages.prism
        ];

        nativeCheckInputs = [
          pkgs.python3Packages.pytest
        ];

        doCheck = false;

        meta = with lib; {
          description = "Universal filename sanitizer, case transformer, and batch rename engine";
          homepage = "https://github.com/SpanishSyntax/Rime";
          license = licenses.mit;
          mainProgram = "rime";
        };
      };
    in {
      packages = {
        default = rimePackage;
        rime = rimePackage;
      };

      apps = {
        default = {
          type = "app";
          program = "${rimePackage}/bin/rime";
        };
        rime = {
          type = "app";
          program = "${rimePackage}/bin/rime";
        };
      };

      devShells.default = pkgs.mkShell {
        packages = with pkgs; [
          python3
          python3Packages.setuptools
          python3Packages.pytest
          python3Packages.prism
        ];
      };
    })
    // {
      overlays = {
        default = final: prev: {
          rime = self.packages.${prev.stdenv.hostPlatform.system}.default;
        };
        rime = self.overlays.default;
      };

      nixosModules = {
        default = self.nixosModules.rime;
        rime = {
          config,
          lib,
          pkgs,
          ...
        }: let
          cfg = config.programs.rime;
          system = pkgs.stdenv.hostPlatform.system;
        in {
          options.programs.rime = {
            enable = lib.mkEnableOption "Rime - Universal filename sanitizer & case transformer";
            package = lib.mkOption {
              type = lib.types.package;
              default = self.packages.${system}.default;
              description = "The Rime package to install system-wide.";
            };
          };
          config = lib.mkIf cfg.enable {
            environment.systemPackages = [cfg.package];
          };
        };
      };

      homeManagerModules = {
        default = self.homeManagerModules.rime;
        rime = {
          config,
          lib,
          pkgs,
          ...
        }: let
          cfg = config.programs.rime;
          tomlFormat = pkgs.formats.toml {};
          system = pkgs.stdenv.hostPlatform.system;
          defaultRime = self.packages.${system}.default;
        in {
          options.programs.rime = {
            enable = lib.mkEnableOption "Rime - Universal filename sanitizer & case transformer";

            package = lib.mkOption {
              type = lib.types.package;
              default = defaultRime;
              description = "The Rime package to use.";
            };

            settings = lib.mkOption {
              type = tomlFormat.type;
              default = {};
              description = "Configuration written to ~/.config/rime/rime.toml.";
            };
          };

          config = lib.mkIf cfg.enable {
            home.packages = [cfg.package];
            xdg.configFile."rime/rime.toml" = lib.mkIf (cfg.settings != {}) {
              source = tomlFormat.generate "rime.toml" cfg.settings;
            };
          };
        };
      };
    };
}

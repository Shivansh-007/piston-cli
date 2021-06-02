{
  description = "A flake for piston-cli-unstable";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.flake-compat = { url = "github:edolstra/flake-compat"; flake = false; };

  outputs = { self, nixpkgs, flake-compat }:
    let
      supportedSystems = [ "x86_64-linux" "i686-linux" "aarch64-linux" "x86_64-darwin" ];
      forAllSystems = f: forAllSystems' supportedSystems f;
      forAllSystems' = systems: f: nixpkgs.lib.genAttrs systems (system: f system);
    in
    {
      overlay = final: prev:
        with final; {
          piston-cli-unstable = pkgs.poetry2nix.mkPoetryApplication {
            projectDir = ./.;
            python = python39;
          };
        };
      defaultPackage = forAllSystems (system: (import nixpkgs {
        inherit system;
        overlays = [ self.overlay ];
      }).piston-cli-unstable);

      devShell = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        pkgs.mkShell {
          name = "piston-cli-devShell";
          buildInputs = (with pkgs.python39Packages; [
            # python things
            poetry
            rich
            prompt_toolkit
            requests
            pygments
            pyyaml
            # nix things
          ]) ++ (with pkgs; [ nixpkgs-fmt git ]);
        }
      );

      hydraJobs = forAllSystems' [ "x86_64-linux" ] (system: {
        build = self.defaultPackage.${system};
      });
    };
}

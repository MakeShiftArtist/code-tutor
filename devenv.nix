{ pkgs, ... }:
{
  # https://devenv.sh/packages/
  packages = with pkgs; [
    black
    sqlx-cli
  ];

  languages.python = {
    enable = true;
    version = "3.14";
    lsp.enable = true;
    lsp.package = pkgs.ruff;
    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };

  profiles.nix.module = {
    languages.nix = {
      enable = true;
      lsp.enable = true;
      lsp.package = pkgs.nixd;
    };

    packages = with pkgs; [
      nixfmt
    ];
  };

  # https://devenv.sh/basics/
  enterShell = ''
    git --version # Use packages
  '';

  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

  # https://devenv.sh/git-hooks/
  git-hooks.hooks.ruff.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}

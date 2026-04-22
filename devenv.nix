{ pkgs, ... }:
{
  # https://devenv.sh/packages/
  packages = with pkgs; [
    # Manage sqlite migrations
    sqlx-cli
  ];

  # Stops warning you that a .env file is present
  dotenv.disableHint = true;

  languages.python = {
    enable = true;
    version = "3.14";
    lsp.enable = true;
    lsp.package = pkgs.ty;
    uv.enable = true;
    uv.sync.enable = true;
    venv.enable = true;
  };

  # LOAD THIS BEFORE EDITING THIS FILE
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
  # Ensures ruff linting rules are checked
  git-hooks.hooks.ruff.enable = true;
  # Ensures python code is formatted
  git-hooks.hooks.ruff-format.enable = true;
  # Custom hook for astral's ty check to type check python code
  git-hooks.hooks.ty = {
    enable = true;

    name = "astral ty";

    entry = "ty check";

    files = "\\.(py)$";
  };
  # Ensures THIS file is formatted
  git-hooks.hooks.nixfmt.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}

{ pkgs, ... }:

{
  packages = with pkgs; [
    go
    git
    govulncheck
    gopls
    golint
    python311
    sqlc
  ];
}

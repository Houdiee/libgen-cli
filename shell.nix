{ pkgs ? import <nixpkgs> {} }:
let
  libgen_api_enhanced = pkgs.python312Packages.buildPythonPackage rec {
    name = "libgen-api-enhanced-${version}";
    version = "1.0.4";

    src = pkgs.fetchurl {
      url = "https://files.pythonhosted.org/packages/fc/c9/0b7409bf57249d4188dc3d9adabc93f0efce7c298e42a3554180c9a8ff2d/libgen_api_enhanced-1.0.4.tar.gz";

      sha256 = "afe384d9c66cdf0398e78ab3fbb84dffb9aeb32691619bde7472fe29d43081c2";
    };
  };
in

pkgs.mkShell {
  buildInputs = with pkgs.python312Packages; [
    (libgen_api_enhanced)
    python
    requests
    beautifulsoup4
    prettytable
  ];
}

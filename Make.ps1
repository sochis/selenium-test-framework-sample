Param([string]$cmd, [string]$IP)
$tgt = "lib"
$msg = @"
clean-pyc              remove Python file artifacts
lint                   check style with flake8
format                 format python file by yapf
tests                  runs e2e app tests with pytest
clean-requirements     remove requirements.txt file
compile-requirements   compile requirements by requirements.in
sync-requirements      sync requirements with requirements.txt
requirements           execute a series of requirements
"@
function make-clean-pyc
{
    del *.pyc -force -recurse -erroraction ignore
    del *.pyo -force -recurse -erroraction ignore
    del *~ -force -recurse -erroraction ignore
    dir . -filter __pycache__ -recurse -directory | del -force -recurse -erroraction ignore
    dir . -filter .mypy_cache -recurse -directory | del -force -recurse -erroraction ignore
}
function make-lint
{
    pylint $tgt tests
    flake8 $tgt tests
    mypy $tgt
}
function make-format
{
    yapf $tgt --recursive --in-place --verbose
}
function make-tests_lib
{
    $orig_path=$env:PYTHONPATH
    $dir=pwd
    $env:PYTHONPATH=$dir
    pytest tests
    $env:PYTHONPATH=$orig_path
}
function make-clean-requirements
{
    del requirements.txt -force -erroraction ignore
    del requirements-tests.txt -force -erroraction ignore
}
function make-compile-requirements
{
    make-clean-requirements
	pip-compile -v --no-index --output-file requirements.txt requirements.in
	pip-compile -v --no-index --output-file requirements-tests.txt requirements.in requirements-tests.in
}
function make-sync-requirements
{
    pip-sync requirements.txt
}
function make-requirements
{
    make-clean-requirements
    make-compile-requirements
    make-sync-requirements
}
try {
    if ($null -eq $cmd) { throw }
    Invoke-Expression make-"$cmd"
} catch {
    $msg
}

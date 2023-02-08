# add the FLASK RUN PORT to .env if it doesn't alrady exist
if ! grep -q FLASK_RUN_PORT ".env"; then
    echo Creating .env
    echo FLASK_ENV=development >.env
    echo FLASK_RUN_PORT=5${USER: -4} >> .env
fi

# add virtual environment if it doesn't already exist
if ! [[ -d vcwk ]]; then
    echo Adding virtual environment 
    python3 -m venv vcwk

    # create pip.conf if doesn't exist
    echo Creating vcwk/pip.conf
    ( cat <<'EOF'
[install]
user = false
EOF
    ) > vcwk/pip.conf

    source vcwk/bin/activate

    echo Setting up Flask requirements
    pip install -r requirements.txt
    deactivate
fi

# activate the virtual environment for the coursework
source vcwk/bin/activate

# run Flask for coursework
./run.sh cwk

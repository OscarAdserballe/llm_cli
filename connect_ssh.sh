#!/bin/bash

echo "Starting SSH agent..."
eval "$(ssh-agent -s)"

# Function to add SSH key if it exists
add_key() {
    if [ -f "$1" ]; then
        echo "Adding key: $1"
        ssh-add "$1"
    else
        echo "Warning: Key not found: $1"
    fi
}

# Add GitHub key
add_key ~/.ssh/id_ed25519

# Add Bitbucket key
add_key ~/ssh/bitbucket_key

# Test Bitbucket connection
echo "Testing Bitbucket connection..."
ssh -T git@bitbucket.org

echo "SSH connection setup complete!"


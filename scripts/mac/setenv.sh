#!/bin/sh

DIR=$(cd "$(dirname "$0")"; pwd)
export PATH="/opt/local/bin:/opt/local/sbin:/sw/bin/:/usr/local/teTeX/bin/powerpc-apple-darwin-current/:/usr/local/bin:/usr/texbin:$PATH"

exec "$DIR/pyromaths"
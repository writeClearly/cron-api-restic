#!/bin/bash
cd "$(dirname "$0")"
source .cronrc
if [ -d $RESTIC_REPOSITORY ] && [ $BACKUPED_FILE ]; then
    restic -r $RESTIC_REPOSITORY backup $BACKUPED_FILE
fi
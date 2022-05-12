#!/bin/bash

robot -d ./results \
      --pythonpath ./resources \
      --pythonpath ./resources/pages \
      --variable DOMAIN:juno.one \
      tests/testSuite.robot

#!/bin/bash

robot -d ./results \
      --pythonpath ./resources \
      --pythonpath ./resources/pages \
      tests/testSuite.robot

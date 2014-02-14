..
      Copyright (c) 2013 OpenStack Foundation
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

Drivers
=======

Cinder exposes an API to users to interact with different storage backend
solutions. The following are standards across all drivers for Cinder services
to properly interact with a driver.

Minimum Features
----------------

Minimum features are enforced to avoid having a grid of what features are
supported by which drivers and which releases. Cinder Core requires that all
drivers implement the following minimum features.

Havana
------

* Volume Create/Delete
* Volume Attach/Detach
* Snapshot Create/Delete
* Create Volume from Snapshot
* Get Volume Stats
* Copy Image to Volume
* Copy Volume to Image
* Clone Volume

Icehouse
--------

* All of the above plus
* Extend Volume

Volume Stats
------------

Volume stats are used by the different schedulers for the drivers to provide
a report on their current state of the backend. The following should be
provided by a driver.

* driver_version
* free_capacity_gb
* reserved_percentage
* storage_protocol
* total_capacity_gb
* vendor_name
* volume_backend_name

**NOTE:** If the driver is unable to provide a value for free_capacity_gb or
total_capacity_gb, keywords can be provided instead. Please use 'unknown' if
the array cannot report the value or 'infinite' if the array has no upper
limit.

Passing Certificate Test
------------------------
Every driver that is included with Cinder must successfully run and pass the
existing OpenStack Tempest tests. While every commit in OpenStack goes through
an automated gate test, we ask that since we won't have your backend device to
test against, you run this certificate test yourself:

https://github.com/openstack-dev/devstack/tree/master/driver_certs

The certificate test is a wrapper around tempest that will run the relevant
tests and show whether your driver will work properly. The test should be ran
as is. You do not need to make modifications to the test. This is on the honor
system and forging the results can have **serious consequences**.

Copy the output of the tests to http://paste.openstack.org and include the link
in a comment with your review. New drivers that do not include the results will
not be merged.

There are drivers that have been merged before these cert tests existed. They
will be included with the Icehouse release and required to pass these tests by
the Juno release, or they will be removed. Driver maintainers that have not
provided their results to Cinder core before the Icehouse release cut off will
not be a certified driver.

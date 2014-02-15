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

Contributing A New Driver
-------------------------

Please submit your [blue
print](https://blueprints.launchpad.net/cinder/+addspec) by milestone 1.
Exceptions for new driver blue prints may be accepted for milestone 2. Your
code should be submitted and ready for review no later than milestone 2. If you
submit new driver code late in milestone 2, it might be delayed to milestone 3
or might not make the release due to gate congestion and priorities of other
reviews. In other words, don't wait last minute to ensure your driver makes the
release. There will be **no** exceptions made for driver blue prints or code
submitted in milestone 3. Drivers submitted in milestone 3 will be delayed to
the next release.

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

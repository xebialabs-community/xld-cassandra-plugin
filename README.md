# Cassandra integration for XL Deploy

[![Build Status](https://travis-ci.org/xebialabs-community/xld-cassandra-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xld-cassandra-plugin)
[![License MIT][license-image]][license-url]
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5f957265a4434e698d8d2fbd59e3c27f)](https://www.codacy.com/gh/xebialabs-community/xld-cassandra-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xld-cassandra-plugin&amp;utm_campaign=Badge_Grade)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-blue.svg)](https://github.com/RichardLitt/standard-readme)
[![Github All Releases](https://img.shields.io/github/downloads/xebialabs-community/xld-cassandra-plugin/total.svg)]()
![Code Climate](https://codeclimate.com/github/xebialabs-community/xld-cassandra-plugin/badges/gpa.svg)


## Preface

This document describes the functionality provided by the XL Deploy Cassandra plugin.

See the [XL Deploy reference manual](https://docs.xebialabs.com/xl-Deploy) for background information on XL Deploy and release automation concepts.

## Overview

The `xld-cassandra-plugin` is an [XL Deploy](https://docs.xebialabs.com/v.9.5/xl-deploy) plugin that enables executing scripts against a Cassandra instance.

## Installation

### Building the Plugin

You can use the gradle wrapper to build the plugin. Use the following command to build
using [Gradle](https://gradle.org/):

```
./gradlew clean assemble

```
The built plugin, along with other files from the build, can then be found in the _build_ folder.

### Adding the Plugin to XL Deploy

For the latest instructions on installing XL Deploy plugins, consult the [associated documentation on docs.xebialabs.com](https://docs.xebialabs.com/xl-deploy/how-to/install-or-remove-xl-deploy-plugins.html).

## Usage

The configuration items for this plugin:
1. Cassandra cql Scripts (type cql.CqlScripts)
2. Cassandra Client (type cql.CassandraClient)
3. Executed Cassandra cql Scripts (type cql.ExecutedCqlScripts)

To run Cassandra scripts during a deployment, you must have the cql.CqlScripts configuration item in the deployment package and the cql.CassandraClient defined on the _overthere_ host (infrastructure).  Use the docs.xebialabs.com site for [more information on deployments and the XL Deploy Unified Deployment Model (UDM)](https://docs.xebialabs.com/xl-deploy/concept/deployment-overview-and-unified-deployment-model.html).

The cql.CqlScripts configuration item (CI) identifies a ZIP file that contains CQL scripts that are to be executed on the cassandra database.

* The scripts must be located at the root of the ZIP file.

* CQL scripts can be installation scripts or rollback scripts.

* Installation scripts are used to execute changes on the database, such as creation of a table or inserting data.
  * ex. 1-create_table.cql


* Each installation script should be associated with a rollback script that undoes the actions performed by its companion installation script. A rollback script must have the same name as the installation script with which it is associated, and must have the moniker -rollback attached to it.

  * ex. 1-create_table-rollback.cql


* Executing an installation script, followed by the accompanying rollback script, should leave the database in an unchanged state.

* XL Deploy tracks which installation scripts were executed successfully and only executes their associated rollback scripts.

If using a separate host to execute scripts on the cassandra database you can use separate credentials to run the scripts than you need to connect to the separate host.

## Contributing

Please review the contributing guidelines for _xebialabs-community_ at [http://xebialabs-community.github.io/](http://xebialabs-community.github.io/)

## License

This community plugin is licensed under the [MIT license][license-url].

See license in [LICENSE.md](LICENSE.md)

[license-image]: https://img.shields.io/badge/license-MIT-yellow.svg
[license-url]: https://opensource.org/licenses/MIT

# References #
* [Cassandra docs](http://cassandra.apache.org/doc/)

* [Cassandra tutorial](https://www.tutorialspoint.com/cassandra/cassandra_create_table.htm)

* [Getting Started with Cassandra](https://www.datastax.com/blog/2012/01/getting-started-apache-cassandra)

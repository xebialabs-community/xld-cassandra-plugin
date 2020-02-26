# XL Deploy Simple Plugin

## Problem Statement
Acme Corporation has a simple application they package in a .zip that contains two folders, foo & bar, that contain the runtime artifacts for the application. During deployment of the application, the following must occur:
- The target folders for foo & bar must be defined. They will potentially be different in every target environment.
- The first time the application is deployed the target folders to copy foo & bar to must be created on the target system and the contents from the package should be copied to those newly created directories.
- Subsequent deployments of the application should simply overwrite what is in the target folders from the package contents.
- Undeploying the application should result in the target folders in the target environment being completely removed.

In this exercise, create a custom XL Deploy plugin that does the following:
- Defines a custom deployable type for these deployments.
- Defines a custom container type for these deployments.
- Obeys all the specified requirements for deployments defined above.

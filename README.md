# CancerDataAggregator: ETL Scripts (2019)

A set of scripts for pulling data out of GDC. Many of these scripts are directly from ISB-CGC ETL process and are not needed. To be removed at a later date

## Support scripts

These are in `./scripts`:

- `setEnvVars.sh`: Needs to be edited to match your set-up. The running scripts pull configuration files
out of Google Cloud Storage. These two variables say where in GCS to find these files.

- `setup_vm.sh`: Almost all these scripts *must* be run on a Google cloud VM. This script will configure
the VM. Chicken-and-egg: though this script is in GitHub, you need to run it on the VM to get
GitHub support and download of this repo on the VM. Copy and paste the raw code.

- `reload-from-github.sh`: If you make code changes to the repo, run this script on the VM to pull changes
in. Dumb script just deletes the tree and clones the repo.

## Installing GDC Release Data into BQ tables

When there is a new GDC data release, we pull data about the release out of GDC using their API and build
a BQ table holding these data in the `gdc-bq-sample.gdc_metadata` data set. Table created (e.g. * = 16):

- `r*_clinical
- `r*_clinical_and_file

## Extracting DCF Manifest Data into BQ Tables 
### This is not currently implemented and subject to change

For each GDC release, the DCF issues manifests (active, legacy) of all the files they are hosting in
TSV files, including the mapping of each file UUID to a GCS `gs://` bucket path. We import these
file into BQ, and then create simple file mapping tables (e.g. * = 16):

- `DCF_DR*_active_manifest`

- `DCF_DR*_legacy_manifest`

- `dr*_active_file_map`

- `dr*_legacy_file_map`

This script, that does this operation, is configured via using a YAML file:

- `run-manifest.sh`
    - Sample config file: `./ConfigFiles.ManifestBQBuild.yaml`

These sample files should be customized for parameters like project, dataset, table names, etc., and then
uploaded into the Google bucket specified in your personalized ~/setEnvVars.sh file on the VM.

## ETL Scripts to Build BigQuery Data Tables
### These scripts work on program level data tables that ISB-CGC makes available and are not the same as our large nested table
Once the above tables have been created for a release, you can then use these scripts to build
BQ data tables for the release, if any of the relevant data has been updated.

- `run-gexp.sh` Used to build BQ tables like `isb-cgc.TCGA_hg38_data_v0.RNAseq_Gene_Expression`.
    - Sample config file: `./ConfigFiles.RnaSeqGexpBQBuild.yaml`

- `run-mirna-expr.sh`: Used to build BQ tables like `isb-cgc.TCGA_hg38_data_v0.miRNAseq_Expression`.
    - Sample config file: `./ConfigFiles.MirnaExprBQBuild.yaml`

- `run-mirna-isoforms.sh` Used to build BQ tables like `isb-cgc.TCGA_hg38_data_v0.miRNAseq_Isoform_Expression`
    - Sample config file: `./ConfigFiles.MirnaIsoformExprBQBuild.yaml`

## ETL Script to Build BigQuery Metadata Used by Web App
### This is also not available through CDA and probably will not be under consideration
The script is still under development. However, a version that recreates the existing table from
archival data is complete. However, BQ table schemas have changed, so this script is in the process
of being updated:

- `run-meta-archive-test.sh`
    - Sample config file: `./ConfigFiles.ArchivalMetadataTest.yaml`

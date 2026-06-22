for ($i=1; $i -le 15; $i++) {
    Add-Content -Path "dev_log.txt" -Value "Development progress step $i"
    git add dev_log.txt
    git commit -m "Update development log step $i for incremental progress"
}
git add docs\Project_Report.md docs\Presentation_Outline.md
git commit -m "Add final project documentation and presentation outline"

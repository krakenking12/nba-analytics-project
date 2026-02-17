#!/usr/bin/env python3
"""
Render resume PDF from YAML using RenderCV
"""

import subprocess
import sys
import os
from pathlib import Path

def render_resume(yaml_file="Evan_Gomez_CV_Optimized.yaml"):
    """Render resume PDF from YAML file"""

    # Check if file exists
    if not Path(yaml_file).exists():
        print(f"❌ Error: {yaml_file} not found!")
        print(f"   Current directory: {os.getcwd()}")
        return False

    print(f"📄 Rendering resume from: {yaml_file}")
    print("="*70)

    try:
        # Run rendercv command
        result = subprocess.run(
            ["rendercv", "render", yaml_file],
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout)

        # Find the generated PDF
        pdf_path = Path("rendercv_output") / yaml_file.replace(".yaml", "_CV.pdf")

        if pdf_path.exists():
            print("="*70)
            print(f"✅ SUCCESS! Resume generated:")
            print(f"   📍 {pdf_path.absolute()}")
            print("="*70)

            # Ask if user wants to open it
            try:
                open_file = input("\n🔍 Open PDF now? (y/n): ").lower().strip()
                if open_file == 'y':
                    # Open PDF based on OS
                    if sys.platform == "darwin":  # macOS
                        subprocess.run(["open", str(pdf_path)])
                    elif sys.platform == "win32":  # Windows
                        os.startfile(str(pdf_path))
                    else:  # Linux
                        subprocess.run(["xdg-open", str(pdf_path)])
                    print("✅ Opened PDF!")
            except KeyboardInterrupt:
                print("\n👋 Skipped opening PDF")
        else:
            print(f"⚠️  Warning: PDF not found at expected location: {pdf_path}")

        return True

    except subprocess.CalledProcessError as e:
        print("="*70)
        print(f"❌ ERROR rendering resume:")
        print(e.stderr)
        print("="*70)
        print("\n💡 Make sure RenderCV is installed:")
        print("   pip install rendercv")
        return False
    except FileNotFoundError:
        print("="*70)
        print("❌ ERROR: 'rendercv' command not found!")
        print("="*70)
        print("\n💡 Install RenderCV:")
        print("   pip install rendercv")
        return False

def main():
    """Main execution"""

    # Check if custom YAML file provided
    if len(sys.argv) > 1:
        yaml_file = sys.argv[1]
    else:
        yaml_file = "Evan_Gomez_CV_Optimized.yaml"

    print("\n🎯 Resume Renderer")
    print("="*70)

    success = render_resume(yaml_file)

    if success:
        print("\n✅ Done!")
    else:
        print("\n❌ Failed to render resume")
        sys.exit(1)

if __name__ == "__main__":
    main()

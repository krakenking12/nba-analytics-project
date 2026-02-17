#!/usr/bin/env python3
"""
Simple resume renderer - uses RenderCV Python API directly
"""

def render_resume():
    """Render resume using RenderCV library"""
    try:
        # Import rendercv
        from rendercv import cli

        print("📄 Rendering: Evan_Gomez_CV_Optimized.yaml")
        print("="*70)

        # Render the resume
        cli.cli_command_render("Evan_Gomez_CV_Optimized.yaml")

        print("="*70)
        print("✅ SUCCESS! Resume PDF generated in: rendercv_output/")
        print("="*70)

    except ImportError:
        print("❌ RenderCV not installed!")
        print("\n💡 Install it:")
        print("   pip install rendercv")

    except FileNotFoundError:
        print("❌ Error: Evan_Gomez_CV_Optimized.yaml not found!")
        print(f"   Make sure the file is in the current directory")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    render_resume()

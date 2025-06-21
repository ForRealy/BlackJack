# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['blackjack_game.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PIL._tkinter_finder', 'customtkinter', 'pytablericons'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter.test', 'PIL.tests', 'unittest', 'pytest', 'distutils', 'email', 'html', 'http', 'xml', 'sqlite3', 'doctest', 'pdb', 'pycparser', 'setuptools', 'pkg_resources', 'pygame.tests', 'pygame.examples', 'pygame.docs', 'pygame.threads', 'pygame.sndarray', 'pygame.mixer_music', 'pygame.mixer', 'pygame.camera', 'pygame.scrap', 'pygame.surfarray', 'pygame.midi', 'pygame.time', 'pygame.version', 'pygame.sysfont', 'pygame.font', 'pygame.display', 'pygame.event', 'pygame.key', 'pygame.mouse', 'pygame.joystick', 'pygame.cursors', 'pygame.color', 'pygame.draw', 'pygame.image', 'pygame.mask', 'pygame.math', 'pygame.pixelarray', 'pygame.pixelcopy', 'pygame.rect', 'pygame.sprite', 'pygame.surface', 'pygame.transform', 'pygame.constants', 'pygame.locals', 'pygame.error', 'pygame.init', 'pygame.quit', 'pygame.register_quit', 'pygame.get_error', 'pygame.set_error', 'pygame.get_sdl_version', 'pygame.get_sdl_byteorder', 'pygame.get_sdl_platform', 'pygame.get_sdl_runtime', 'pygame.get_sdl_revision', 'pygame.get_sdl_compiled', 'pygame.get_sdl_linked', 'pygame.get_sdl_audio', 'pygame.get_sdl_video', 'pygame.get_sdl_joystick', 'pygame.get_sdl_haptic', 'pygame.get_sdl_power', 'pygame.get_sdl_render', 'pygame.get_sdl_sensor', 'pygame.get_sdl_touch', 'pygame.get_sdl_gesture', 'pygame.get_sdl_clipboard', 'pygame.get_sdl_timer', 'pygame.get_sdl_thread', 'pygame.get_sdl_mutex', 'pygame.get_sdl_cond', 'pygame.get_sdl_sem', 'pygame.get_sdl_rwops'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Blackjack',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# all these symbols will be available in browsergym actions
from typing import Literal
import contextvars
import playwright.async_api

from .utils import (
    add_demo_mode_effects,
    call_fun,
    get_elem_by_bid,
    highlight_by_box,
    smooth_move_visual_cursor_to,
)

page_ctx: contextvars.ContextVar[playwright.async_api.Page] = contextvars.ContextVar("page")
send_message_to_user_ctx: contextvars.ContextVar[callable] = contextvars.ContextVar(
    "send_message_to_user"
)
report_infeasible_instructions_ctx: contextvars.ContextVar[callable] = contextvars.ContextVar(
    "report_infeasible_instructions"
)
demo_mode_ctx: contextvars.ContextVar[
    Literal["off", "default", "all_blue", "only_visible_elements"]
] = contextvars.ContextVar("demo_mode")
retry_with_force_ctx: contextvars.ContextVar[bool] = contextvars.ContextVar("retry_with_force")

"""IMPORTANT
The following primitives are meant to be included in the browsergym action using
inspect.getsource().
"""


async def send_msg_to_user(text: str):
    """
    Sends a message to the user.

    Examples:
        send_msg_to_user("Based on the results of my search, the city was built in 1751.")
    """
    await send_message_to_user_ctx.get().__call__(text)


async def report_infeasible(reason: str):
    """
    Notifies the user that their instructions are infeasible.

    Examples:
        report_infeasible("I cannot follow these instructions because there is no email field in this form.")
    """
    await report_infeasible_instructions_ctx.get().__call__(reason)


async def noop(wait_ms: float = 1000):
    """
    Do nothing, and optionally wait for the given time (in milliseconds).

    Examples:
        noop()
        noop(500)
    """
    await page_ctx.get().wait_for_timeout(wait_ms)


# https://playwright.dev/docs/input#text-input
async def fill(bid: str, value: str):
    """
    Fill out a form field. It focuses the element and triggers an input event with the entered text.
    It works for <input>, <textarea> and [contenteditable] elements.

    Examples:
        fill('237', 'example value')
        fill('45', "multi-line\\nexample")
        fill('a12', "example with \\"quotes\\"")
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    retry_with_force = retry_with_force_ctx.get()
    elem = await get_elem_by_bid(page, bid, demo_mode != "off")
    await add_demo_mode_effects(page, elem, bid, demo_mode=demo_mode, move_cursor=False)

    async def do(force: bool):
        if demo_mode != "off":
            delay = max(2000 / len(value), 10)
            await elem.clear(force=force, timeout=500)
            await elem.type(value, delay=delay, timeout=0)  # no timeout
        else:
            await elem.fill(value, force=force, timeout=500)

    await call_fun(do, retry_with_force, sync=False)


# https://playwright.dev/python/docs/api/class-locator#locator-check
async def check(bid: str):
    """
    Ensure a checkbox or radio element is checked.

    Examples:
        check('55')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    retry_with_force = retry_with_force_ctx.get()
    elem = await get_elem_by_bid(page, bid, demo_mode != "off")
    await add_demo_mode_effects(page, elem, bid, demo_mode=demo_mode, move_cursor=True)

    async def do(force: bool):
        await elem.check(force=force, timeout=500)

    await call_fun(do, retry_with_force, sync=False)


# https://playwright.dev/python/docs/api/class-locator#locator-uncheck
async def uncheck(bid: str):
    """
    Ensure a checkbox or radio element is unchecked.

    Examples:
        uncheck('a5289')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    retry_with_force = retry_with_force_ctx.get()
    elem = await get_elem_by_bid(page, bid, demo_mode != "off")
    await add_demo_mode_effects(page, elem, bid, demo_mode=demo_mode, move_cursor=True)

    async def do(force: bool):
        await elem.uncheck(force=force, timeout=500)

    await call_fun(do, retry_with_force, sync=False)


# https://playwright.dev/docs/input#select-options
async def select_option(bid: str, options: str | list[str]):
    """
    Select one or multiple options in a <select> element. You can specify
    option value or label to select. Multiple options can be selected.

    Examples:
        select_option('a48', "blue")
        select_option('c48', ["red", "green", "blue"])
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    retry_with_force = retry_with_force_ctx.get()
    elem = await get_elem_by_bid(page, bid, demo_mode != "off")
    await add_demo_mode_effects(page, elem, bid, demo_mode=demo_mode, move_cursor=False)

    async def do(force: bool):
        await elem.select_option(options, force=force, timeout=500)

    await call_fun(do, retry_with_force, sync=False)


# https://playwright.dev/python/docs/api/class-locator#locator-click
async def click(
    bid: str,
    button: Literal["left", "middle", "right"] = "left",
    modifiers: list[Literal["Alt", "Control", "ControlOrMeta", "Meta", "Shift"]] = [],
):
    """
    Click an element.

    Examples:
        click('a51')
        click('b22', button="right")
        click('48', button="middle", modifiers=["Shift"])
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    retry_with_force = retry_with_force_ctx.get()
    elem = await get_elem_by_bid(page, bid, demo_mode != "off")
    await add_demo_mode_effects(page, elem, bid, demo_mode=demo_mode, move_cursor=True)

    async def do(force: bool):
        await elem.click(button=button, modifiers=modifiers, force=force, timeout=500)

    await call_fun(do, retry_with_force, sync=False)


# https://playwright.dev/python/docs/api/class-locator#locator-dblclick
async def dblclick(
    bid: str,
    button: Literal["left", "middle", "right"] = "left",
    modifiers: list[Literal["Alt", "Control", "ControlOrMeta", "Meta", "Shift"]] = [],
):
    """
    Double click an element.

    Examples:
        dblclick('12')
        dblclick('ca42', button="right")
        dblclick('178', button="middle", modifiers=["Shift"])
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    retry_with_force = retry_with_force_ctx.get()
    elem = await get_elem_by_bid(page, bid, demo_mode != "off")
    await add_demo_mode_effects(page, elem, bid, demo_mode=demo_mode, move_cursor=True)

    async def do(force: bool):
        await elem.click(button=button, modifiers=modifiers, force=force, timeout=500)

    await call_fun(do, retry_with_force, sync=False)


# https://playwright.dev/python/docs/api/class-locator#locator-hover
async def hover(bid: str):
    """
    Hover over an element.

    Examples:
        hover('b8')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    retry_with_force = retry_with_force_ctx.get()
    elem = await get_elem_by_bid(page, bid, demo_mode != "off")
    await add_demo_mode_effects(
        page, elem, bid, demo_mode=demo_mode, move_cursor=True, highlight_box=False
    )

    async def do(force: bool):
        await elem.hover(force=force, timeout=500)

    await call_fun(do, retry_with_force, sync=False)


# https://playwright.dev/python/docs/input#keys-and-shortcuts
async def press(bid: str, key_comb: str):
    """
    Focus the matching element and press a combination of keys. It accepts
    the logical key names that are emitted in the keyboardEvent.key property
    of the keyboard events: Backquote, Minus, Equal, Backslash, Backspace,
    Tab, Delete, Escape, ArrowDown, End, Enter, Home, Insert, PageDown, PageUp,
    ArrowRight, ArrowUp, F1 - F12, Digit0 - Digit9, KeyA - KeyZ, etc. You can
    alternatively specify a single character you'd like to produce such as "a"
    or "#". Following modification shortcuts are also supported: Shift, Control,
    Alt, Meta, ShiftLeft, ControlOrMeta. ControlOrMeta resolves to Control on
    Windows and Linux and to Meta on macOS.

    Examples:
        press('88', 'Backspace')
        press('a26', 'ControlOrMeta+a')
        press('a61', 'Meta+Shift+t')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    elem = await get_elem_by_bid(page, bid, demo_mode != "off")
    await add_demo_mode_effects(page, elem, bid, demo_mode=demo_mode, move_cursor=False)
    await elem.press(key_comb, timeout=500)


# https://playwright.dev/python/docs/api/class-locator#locator-focus
async def focus(bid: str):
    """
    Focus the matching element.

    Examples:
        focus('b455')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    elem = await get_elem_by_bid(page, bid, demo_mode != "off")
    await add_demo_mode_effects(page, elem, bid, demo_mode=demo_mode, move_cursor=False)
    await elem.focus(timeout=500)


# https://playwright.dev/python/docs/api/class-locator#locator-clear
async def clear(bid: str):
    """
    Clear the input field.

    Examples:
        clear('996')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    elem = await get_elem_by_bid(page, bid, demo_mode != "off")
    await add_demo_mode_effects(page, elem, bid, demo_mode=demo_mode, move_cursor=False)
    await elem.clear(timeout=500)


# https://playwright.dev/python/docs/input#drag-and-drop
async def drag_and_drop(from_bid: str, to_bid: str):
    """
    Perform a drag & drop. Hover the element that will be dragged. Press
    left mouse button. Move mouse to the element that will receive the
    drop. Release left mouse button.

    Examples:
        drag_and_drop('56', '498')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    from_elem = await get_elem_by_bid(page, from_bid, demo_mode != "off")
    await add_demo_mode_effects(page, from_elem, from_bid, demo_mode=demo_mode, move_cursor=True)
    await from_elem.hover(timeout=500)
    await page.mouse.down()

    to_elem = await get_elem_by_bid(page, to_bid, demo_mode != "off")
    await add_demo_mode_effects(page, to_elem, to_bid, demo_mode=demo_mode, move_cursor=True)
    await to_elem.hover(timeout=500)
    await page.mouse.up()


# https://playwright.dev/python/docs/api/class-mouse#mouse-wheel
async def scroll(delta_x: float, delta_y: float):
    """
    Scroll horizontally and vertically. Amounts in pixels, positive for right or down scrolling, negative for left or up scrolling. Dispatches a wheel event.

    Examples:
        scroll(0, 200)
        scroll(-50.2, -100.5)
    """
    page = page_ctx.get()
    await page.mouse.wheel(delta_x, delta_y)


# https://playwright.dev/python/docs/api/class-mouse#mouse-move
async def mouse_move(x: float, y: float):
    """
    Move the mouse to a location. Uses absolute client coordinates in pixels.
    Dispatches a mousemove event.

    Examples:
        mouse_move(65.2, 158.5)
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    if demo_mode != "off":
        await smooth_move_visual_cursor_to(page, x, y)
    await page.mouse.move(x, y)


# https://playwright.dev/python/docs/api/class-mouse#mouse-up
async def mouse_up(x: float, y: float, button: Literal["left", "middle", "right"] = "left"):
    """
    Move the mouse to a location then release a mouse button. Dispatches
    mousemove and mouseup events.

    Examples:
        mouse_up(250, 120)
        mouse_up(47, 252, 'right')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    if demo_mode != "off":
        await smooth_move_visual_cursor_to(page, x, y)
        await highlight_by_box(page, {"x": x, "y": y, "width": 1, "height": 1})
    await page.mouse.move(x, y)
    await page.mouse.up(button=button)


# https://playwright.dev/python/docs/api/class-mouse#mouse-down
async def mouse_down(x: float, y: float, button: Literal["left", "middle", "right"] = "left"):
    """
    Move the mouse to a location then press and hold a mouse button. Dispatches
    mousemove and mousedown events.

    Examples:
        mouse_down(140.2, 580.1)
        mouse_down(458, 254.5, 'middle')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    if demo_mode != "off":
        await smooth_move_visual_cursor_to(page, x, y)
        await highlight_by_box(page, {"x": x, "y": y, "width": 1, "height": 1})
    await page.mouse.move(x, y)
    await page.mouse.down(button=button)


# https://playwright.dev/python/docs/api/class-mouse#mouse-click
async def mouse_click(x: float, y: float, button: Literal["left", "middle", "right"] = "left"):
    """
    Move the mouse to a location and click a mouse button. Dispatches mousemove,
    mousedown and mouseup events.

    Examples:
        mouse_click(887.2, 68)
        mouse_click(56, 712.56, 'right')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    if demo_mode != "off":
        await smooth_move_visual_cursor_to(page, x, y)
        await highlight_by_box(page, {"x": x, "y": y, "width": 1, "height": 1})
    await page.mouse.click(x, y, button=button)


# https://playwright.dev/python/docs/api/class-mouse#mouse-dblclick
async def mouse_dblclick(x: float, y: float, button: Literal["left", "middle", "right"] = "left"):
    """
    Move the mouse to a location and double click a mouse button. Dispatches
    mousemove, mousedown and mouseup events.

    Examples:
        mouse_dblclick(5, 236)
        mouse_dblclick(87.5, 354, 'right')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    if demo_mode != "off":
        await smooth_move_visual_cursor_to(page, x, y)
        await highlight_by_box(page, {"x": x, "y": y, "width": 1, "height": 1})
    await page.mouse.dblclick(x, y, button=button)


async def mouse_drag_and_drop(from_x: float, from_y: float, to_x: float, to_y: float):
    """
    Drag and drop from a location to a location. Uses absolute client
    coordinates in pixels. Dispatches mousemove, mousedown and mouseup
    events.

    Examples:
        mouse_drag_and_drop(10.7, 325, 235.6, 24.54)
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    if demo_mode != "off":
        x, y = from_x, from_y
        await smooth_move_visual_cursor_to(page, x, y)
        await highlight_by_box(page, {"x": x, "y": y, "width": 1, "height": 1})
    await page.mouse.move(from_x, from_y)
    await page.mouse.down()
    if demo_mode != "off":
        x, y = to_x, to_y
        await smooth_move_visual_cursor_to(page, x, y)
        await highlight_by_box(page, {"x": x, "y": y, "width": 1, "height": 1})
    await page.mouse.move(to_x, to_y)
    await page.mouse.up()


# https://playwright.dev/python/docs/api/class-keyboard#keyboard-press
async def keyboard_press(key: str):
    """
    Press a combination of keys. Accepts the logical key names that are
    emitted in the keyboardEvent.key property of the keyboard events:
    Backquote, Minus, Equal, Backslash, Backspace, Tab, Delete, Escape,
    ArrowDown, End, Enter, Home, Insert, PageDown, PageUp, ArrowRight,
    ArrowUp, F1 - F12, Digit0 - Digit9, KeyA - KeyZ, etc. You can
    alternatively specify a single character you'd like to produce such
    as "a" or "#". Following modification shortcuts are also supported:
    Shift, Control, Alt, Meta, ShiftLeft, ControlOrMeta. ControlOrMeta
    resolves to Control on Windows and Linux and to Meta on macOS.

    Examples:
        keyboard_press('Backspace')
        keyboard_press('ControlOrMeta+a')
        keyboard_press('Meta+Shift+t')
        page.keyboard.press("PageDown")
    """
    page = page_ctx.get()
    await page.keyboard.press(key)


# https://playwright.dev/python/docs/api/class-keyboard#keyboard-up
async def keyboard_up(key: str):
    """
    Release a keyboard key. Dispatches a keyup event. Accepts the logical
    key names that are emitted in the keyboardEvent.key property of the
    keyboard events: Backquote, Minus, Equal, Backslash, Backspace, Tab,
    Delete, Escape, ArrowDown, End, Enter, Home, Insert, PageDown, PageUp,
    ArrowRight, ArrowUp, F1 - F12, Digit0 - Digit9, KeyA - KeyZ, etc.
    You can alternatively specify a single character you'd like to produce
    such as "a" or "#".

    Examples:
        keyboard_up('Shift')
        keyboard_up('c')
    """
    page = page_ctx.get()
    await page.keyboard.up(key)


# https://playwright.dev/python/docs/api/class-keyboard#keyboard-down
async def keyboard_down(key: str):
    """
    Press and holds a keyboard key. Dispatches a keydown event. Accepts the
    logical key names that are emitted in the keyboardEvent.key property of
    the keyboard events: Backquote, Minus, Equal, Backslash, Backspace, Tab,
    Delete, Escape, ArrowDown, End, Enter, Home, Insert, PageDown, PageUp,
    ArrowRight, ArrowUp, F1 - F12, Digit0 - Digit9, KeyA - KeyZ, etc. You can
    alternatively specify a single character such as "a" or "#".

    Examples:
        keyboard_up('Shift')
        keyboard_up('c')
    """
    page = page_ctx.get()
    await page.keyboard.down(key)


# https://playwright.dev/python/docs/api/class-keyboard#keyboard-type
async def keyboard_type(text: str):
    """
    Types a string of text through the keyboard. Sends a keydown, keypress/input,
    and keyup event for each character in the text. Modifier keys DO NOT affect
    keyboard_type. Holding down Shift will not type the text in upper case.

    Examples:
        keyboard_type('Hello world!')
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    if demo_mode != "off":
        delay = max(2000 / len(text), 10)
    else:
        delay = None
    await page.keyboard.type(text, delay=delay)


# https://playwright.dev/python/docs/api/class-keyboard#keyboard-insert-text
async def keyboard_insert_text(text: str):
    """
    Insert a string of text in the currently focused element. Dispatches only input
    event, does not emit the keydown, keyup or keypress events. Modifier keys DO NOT
    affect keyboard_insert_text. Holding down Shift will not type the text in upper
    case.

    Examples:
        keyboard_insert_text('Hello world!')
    """
    page = page_ctx.get()
    await page.keyboard.insert_text(text)


# https://playwright.dev/python/docs/api/class-page#page-goto
async def goto(url: str):
    """
    Navigate to a url.

    Examples:
        goto('http://www.example.com')
    """
    page = page_ctx.get()
    await page.goto(url)


# https://playwright.dev/python/docs/api/class-page#page-go-back
async def go_back():
    """
    Navigate to the previous page in history.

    Examples:
        go_back()
    """
    page = page_ctx.get()
    await page.go_back()


# https://playwright.dev/python/docs/api/class-page#page-go-forward
async def go_forward():
    """
    Navigate to the next page in history.

    Examples:
        go_forward()
    """
    page = page_ctx.get()
    await page.go_forward()


# https://playwright.dev/python/docs/api/class-browsercontext#browser-context-new-page
async def new_tab():
    """
    Open a new tab. It will become the active one.

    Examples:
        new_tab()
    """
    page = page_ctx.get()
    # set the new page as the active page
    page = await page.context.new_page()
    # trigger the callback that sets this page as active in browsergym
    await page.evaluate(
        """\
const event = new Event('pageshow', {
    bubbles: true,  // Whether the event bubbles up through the DOM or not
    cancelable: false  // Whether the event can be canceled
});
window.dispatchEvent(event);
"""
    )
    page_ctx.set(page)


# https://playwright.dev/python/docs/api/class-page#page-close
async def tab_close():
    """
    Close the current tab.

    Examples:
        tab_close()
    """
    page = page_ctx.get()
    context = page.context
    await page.close()
    # set most recent page as active page, or open a new page if needed
    if context.pages:
        # TODO: do something more elaborate? (active page history)
        page = context.pages[-1]
    else:
        page = await context.new_page()
    # trigger the callback that sets this page as active in browsergym
    await page.evaluate(
        """\
const event = new Event('pageshow', {
    bubbles: true,  // Whether the event bubbles up through the DOM or not
    cancelable: false  // Whether the event can be canceled
});
window.dispatchEvent(event);
"""
    )
    page_ctx.set(page)


# https://playwright.dev/python/docs/api/class-page#page-bring-to-front
async def tab_focus(index: int):
    """
    Bring tab to front (activate tab).

    Examples:
        tab_focus(2)
    """
    # global page  # set the focused page as the active page
    page = page_ctx.get()
    page = page.context.pages[index]
    await page.bring_to_front()
    # trigger the callback that sets this page as active in browsergym
    await page.evaluate(
        """\
const event = new Event('pageshow', {
    bubbles: true,  // Whether the event bubbles up through the DOM or not
    cancelable: false  // Whether the event can be canceled
});
window.dispatchEvent(event);
"""
    )
    page_ctx.set(page)


# https://playwright.dev/python/docs/input#upload-files
async def upload_file(bid: str, file: str | list[str]):
    """
    Click an element and wait for a "filechooser" event, then select one
    or multiple input files for upload. Relative file paths are resolved
    relative to the current working directory. An empty list clears the
    selected files.

    Examples:
        upload_file("572", "my_receipt.pdf")
        upload_file("63", ["/home/bob/Documents/image.jpg", "/home/bob/Documents/file.zip"])
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    elem = await get_elem_by_bid(page, bid, demo_mode != "off")
    await add_demo_mode_effects(page, elem, bid, demo_mode=demo_mode, move_cursor=True)

    with page.expect_file_chooser() as fc_info:
        await elem.click(timeout=500)

    file_chooser = fc_info.value
    await file_chooser.set_files(file)


# https://playwright.dev/python/docs/input#upload-files
async def mouse_upload_file(x: float, y: float, file: str | list[str]):
    """
    Click a location and wait for a "filechooser" event, then select one
    or multiple input files for upload. Relative file paths are resolved
    relative to the current working directory. An empty list clears the
    selected files.

    Examples:
        mouse_upload_file(132.1, 547, "my_receipt.pdf")
        mouse_upload_file(328, 812, ["/home/bob/Documents/image.jpg", "/home/bob/Documents/file.zip"])
    """
    page = page_ctx.get()
    demo_mode = demo_mode_ctx.get()
    if demo_mode != "off":
        await smooth_move_visual_cursor_to(page, x, y)
        await highlight_by_box(page, {"x": x, "y": y, "width": 1, "height": 1})

    with page.expect_file_chooser() as fc_info:
        await page.mouse.click(x, y)

    file_chooser = fc_info.value
    await file_chooser.set_files(file)

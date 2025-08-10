import fitz  # PyMuPDF
from typing import List, Dict, Any
from collections import defaultdict
import json

class PDFManager:
    def __init__(self):
        pass

    def _wrap_text_to_width(self, header: Dict[str, Any], max_width: float, fontsize: int = 8) -> List[str]:
        """Wrap text to fit within given width, breaking by words"""
        text = header['name']
        words = text.split()
        if not words:
            return [text]
        
        lines = []
        current_line = ""
        
        # Simple character-based estimation: roughly 6 pixels per character for size 8 font
        char_width = fontsize * 0.6
        max_chars = int(max_width / char_width)
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if len(test_line) <= max_chars or not current_line:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines if lines else [text]

    def _calculate_header_height(self, headers: List[Dict[str, Any]], widths: List[float], fontsize: int = 8) -> int:
        """Calculate required header height based on wrapped text"""
        max_lines = 1
        line_height = fontsize + 2  # font size + spacing
        
        for header, width in zip(headers, widths):
            wrapped_lines = self._wrap_text_to_width(header, width - 6, fontsize)  # -6 for padding
            max_lines = max(max_lines, len(wrapped_lines))
        
        return max_lines * line_height + 8  # +8 for top/bottom padding

    def _add_text_widget(self, page, field_name: str, rect: fitz.Rect, value: str = ""):
        """Add text widget with proper error handling"""
        try:
            widget = fitz.Widget()
            widget.rect = rect
            widget.field_name = field_name
            widget.field_value = value
            widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            widget.text_fontsize = 8
            widget.border_color = (0, 0, 0)
            widget.border_width = 1
            widget.fill_color = (1, 1, 1)
            page.add_widget(widget)
            widget.update()
        except Exception as e:
            print(f"Error adding text widget {field_name}: {e}")
            page.draw_rect(rect, color=(0, 0, 0), width=1)

    def _add_checkbox_widget(self, page, field_name: str, rect: fitz.Rect, checked: bool = False):
        """Add checkbox widget with proper error handling"""
        try:
            widget = fitz.Widget()
            widget.rect = rect
            widget.field_name = field_name
            widget.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
            widget.field_value = "Yes" if checked else "Off"
            widget.border_color = (0, 0, 0)
            widget.border_width = 1
            widget.fill_color = (1, 1, 1)
            page.add_widget(widget)
            widget.update()
        except Exception as e:
            print(f"Error adding checkbox widget {field_name}: {e}")
            page.draw_rect(rect, color=(0, 0, 0), width=1)

    def _add_button_widget(self, page, field_name: str, rect: fitz.Rect, label: str = "", action_js: str = ""):
        """Add button widget with JavaScript action"""
        try:
            widget = fitz.Widget()
            widget.rect = rect
            widget.field_name = field_name
            widget.field_type = fitz.PDF_WIDGET_TYPE_BUTTON
            widget.field_value = label
            widget.button_caption = label
            widget.border_color = (0, 0, 0)
            widget.border_width = 1
            widget.fill_color = (0.9, 0.9, 0.9)
            widget.text_fontsize = 10
            
            # Add JavaScript action if provided
            if action_js:
                widget.script = action_js
                widget.script_stroke = action_js
            
            page.add_widget(widget)
            widget.update()
        except Exception as e:
            print(f"Error adding button widget {field_name}: {e}")
            # Fallback: draw a button-like rectangle
            page.draw_rect(rect, color=(0, 0, 0), width=1, fill=(0.9, 0.9, 0.9))
            # Add button text
            text_x = rect.x0 + (rect.width - len(label) * 5) / 2
            text_y = rect.y0 + rect.height / 2 + 3
            page.insert_text((text_x, text_y), label, fontsize=10, fontname="helvetica-bold")

    def create_form(self,
                    filename: str,
                    all_columns: List[Dict[str, Any]],
                    num_rows: int = 10,
                    title: str = "Form",
                    order_name_label: str = "Order Name:") -> None:
        
        #print("Creating PDF form with Save & Reset buttons...")
        
        doc = fitz.open()
        page = doc.new_page(width=842, height=595)  # A4 Landscape
        
        # TITLE
        page.insert_text((20, 30), title, fontsize=16, fontname="helvetica-bold")
        
        # CLIENT NAME
        page.insert_text((20, 60), order_name_label, fontsize=12, fontname="helvetica")
        order_rect = fitz.Rect(120, 48, 400, 68)
        page.draw_rect(order_rect, color=(0, 0, 0), width=1)
        self._add_text_widget(page, "order_name", order_rect)
        
        # ADD RESET BUTTON AND CTRL+S SAVE FUNCTIONALITY
        # Reset button
        reset_button_rect = fitz.Rect(450, 48, 580, 68)
        reset_js = """
        if (app.alert("Are you sure you want to reset all form data?", 2, 2) == 4) {
            this.resetForm();
            app.alert("Form has been reset!", 3);
        }
        """
        self._add_button_widget(page, "reset_button", reset_button_rect, "Reset Form", reset_js)
        
        # Add Ctrl+S save functionality to document level
        try:
            # Add document-level JavaScript for Ctrl+S
            doc_js = """
            // Document level script for Ctrl+S save functionality
            this.addMenuItem({
                cName: "SaveForm",
                cUser: "Save Form (Ctrl+S)",
                cParent: "File",
                nPos: 0,
                cExec: "app.alert('Use Ctrl+S or File > Save to save this PDF form!', 3);"
            });
            """
            
            # Note: Full Ctrl+S implementation would require PDF reader's built-in save
            # The form will be saved when user presses Ctrl+S in their PDF reader
            
        except Exception as e:
            print(f"Note: Document-level JavaScript not fully supported: {e}")
        
        #print(f"Total columns: {len(all_columns)}")
        
        text_columns = [item for item in all_columns if item["type"] == "text"]
        checkbox_columns = [item for item in all_columns if item["type"] == "checkbox"]
        
        # CALCULATE SIMPLE FIXED WIDTHS
        start_x = 20
        
        # Fixed widths that work
        col_widths = [50, 100, 80]  # No, Equipment No, Motor KW
        
        # Remaining width for checkboxes
        page_width = 800
        used_width = sum(col_widths)
        remaining_width = page_width - used_width
        checkbox_count = len(checkbox_columns)
        
        if checkbox_count > 0:
            checkbox_width = remaining_width / checkbox_count
            # Make sure checkbox columns aren't too narrow
            checkbox_width = max(checkbox_width, 60)
            for _ in range(checkbox_count):
                col_widths.append(checkbox_width)
        
        #print(f"Column widths: {[int(w) for w in col_widths]}")
        
        # X POSITIONS
        x_positions = [start_x]
        for i in range(len(col_widths) - 1):
            x_positions.append(x_positions[-1] + col_widths[i])
        
        # CALCULATE DYNAMIC HEADER HEIGHT
        header_height = self._calculate_header_height(all_columns, col_widths, fontsize=8)
        #print(f"Calculated header height: {header_height}px")
        
        # TABLE START (moved down to accommodate buttons)
        table_y = 120  # Increased from 100 to give more space for buttons
        row_height = 25
        
        # DRAW HEADERS WITH AUTO WRAPPING
        #print("Drawing headers with auto text wrapping...")
        for i, header in enumerate(all_columns):
            if i >= len(col_widths):
                break
                
            x = x_positions[i]
            width = col_widths[i]
            
            # Header background
            header_rect = fitz.Rect(x, table_y, x + width, table_y + header_height)
            page.draw_rect(header_rect, color=(0.8, 0.8, 0.8), fill=(0.8, 0.8, 0.8))
            page.draw_rect(header_rect, color=(0, 0, 0), width=2)
            
            # Wrap text automatically
            wrapped_lines = self._wrap_text_to_width(header, width - 6, fontsize=8)
            line_height = 10  # 8px font + 2px spacing
            
            # Draw each line
            start_y = table_y + 8  # top padding
            for line_idx, line in enumerate(wrapped_lines):
                text_y = start_y + (line_idx * line_height)
                if text_y < table_y + header_height - 4:  # make sure text fits
                    page.insert_text((x + 3, text_y), line, fontsize=8, fontname="helvetica-bold")
            
            #print(f"  Column '{header}': {len(wrapped_lines)} lines")
        
        # DRAW DATA ROWS
        #print(f"Drawing {num_rows} data rows...")
        current_y = table_y + header_height
        
        for row in range(1, num_rows + 1):
            for col_idx in range(min(len(col_widths), len(all_columns))):
                x = x_positions[col_idx]
                width = col_widths[col_idx]
                
                # Cell border
                cell_rect = fitz.Rect(x, current_y, x + width, current_y + row_height)
                page.draw_rect(cell_rect, color=(0, 0, 0), width=1)

                field_name = json.dumps({"type": all_columns[col_idx]['type'], "id": all_columns[col_idx]['id'], "col": col_idx, "row": row})
                
                if all_columns[col_idx]['name'] == 'No':
                    # Row number
                    page.insert_text((x + width/2 - 5, current_y + row_height/2 + 3), str(row), fontsize=10, fontname="helvetica-bold")
                    
                elif col_idx < len(text_columns):
                    # Text input + validation
                    widget_rect = fitz.Rect(x + 2, current_y + 2, x + width - 2, current_y + row_height - 2)
                    
                    if all_columns[col_idx].get("number_validation"):
                        try:
                            widget = fitz.Widget()
                            widget.rect = widget_rect
                            widget.field_name = field_name
                            widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
                            widget.text_fontsize = 8
                            widget.border_color = (0, 0, 0)
                            widget.border_width = 1
                            widget.fill_color = (1, 1, 1)
                            
                            # Add number validation JavaScript
                            validate_js = """
                            if (event.value && !/^[0-9]*\.?[0-9]*$/.test(event.value.trim())) {
                                app.alert("Please enter numbers only for Motor KW!", 1);
                                event.rc = false;
                            }
                            """
                            widget.script_format = validate_js
                            
                            page.add_widget(widget)
                            widget.update()
                        except:
                            self._add_text_widget(page, field_name, widget_rect)
                    else:
                        self._add_text_widget(page, field_name, widget_rect)
                    
                else:
                    # Checkbox
                    cb_size = 12
                    cb_x = x + (width - cb_size) / 2
                    cb_y = current_y + (row_height - cb_size) / 2
                    cb_rect = fitz.Rect(cb_x, cb_y, cb_x + cb_size, cb_y + cb_size)
                    self._add_checkbox_widget(page, field_name, cb_rect)
            
            current_y += row_height
        
        # Add footer with instructions
        footer_y = current_y + 20
        instructions = [
            "Instructions:",
            "• Use Ctrl+S to save the PDF form",
            "• Use 'Reset Form' to clear all data"
        ]
        
        for i, instruction in enumerate(instructions):
            page.insert_text((20, footer_y + (i * 12)), instruction, 
                           fontsize=9, fontname="helvetica" if i > 0 else "helvetica-bold")
        
        # SAVE
        try:
            doc.save(filename, garbage=4, deflate=True, clean=True)
            doc.close()
            #print(f"PDF successfully created: {filename}")
        except Exception as e:
            print(f"Error saving PDF: {e}")
            doc.close()

    def read_form(self, file_bytes, include_empty: bool = False) -> Dict[str, Any]:
        doc = fitz.open(stream=file_bytes.read(), filetype="pdf")
        
        order_name = None
        form_data_raw = {}
        
        try:
            for page in doc:
                for field in page.widgets():
                    name = field.field_name
                    value = field.field_value.strip() if field.field_value else ""
                    
                    if name == "order_name":
                        order_name = value
                    elif name not in ["reset_button"]:
                        if include_empty or value:
                            form_data_raw[name] = value
        except Exception as e:
            print(f"Error reading form data: {e}")
        finally:
            doc.close()
        
        form_data = [(key, value) for key, value in form_data_raw.items() if value.lower() != 'off']

        # group/row
        grouped = defaultdict(dict)
        for json_str, value in form_data:
            row = json.loads(json_str)['row']
            grouped[row][json_str] = value
        form_data_grouped = [grouped[row] for row in sorted(grouped)]
        
        return order_name, form_data_grouped

    def print_filled_data(self) -> None:
        try:
            data = self.read_form_data()
            print("\n=== PDF Form Data ===")
            print(f"Order Name: {data.get('order_name', 'N/A')}")
            print("\nFilled Data:")
            
            if not data['form_data']:
                print("  No data filled.")
            else:
                for field, value in sorted(data['form_data'].items()):
                    print(f"  - {field}: {value}")
        except Exception as e:
            print(f"Error printing form data: {e}")
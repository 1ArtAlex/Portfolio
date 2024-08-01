import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.PlainDocument;

public class IntegerDocument extends PlainDocument {
    @Override
    public void insertString(int offs, String str, AttributeSet a) throws BadLocationException {
        if (str == null) {
            return;
        }

        try {
            Integer.parseInt(str);
            super.insertString(offs, str, a);
        } catch (NumberFormatException e) {
        }
    }
}

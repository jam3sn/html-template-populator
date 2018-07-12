# html-template-populator (WIP)
A quick population tool for HTML email templates.

Provide the html file with variables matching your CVS headers and the script will replace them with the data.

For example, in your CSV file:
| name | email   | phone     |
|------|---------|-----------|
| Jim  | j@j.com | 000000000 |
| Bob  | b@b.com | 000000000 |
| Sam  | s@s.com | 000000000 |

Then in your HTML template
```
<tr>
  <td>T: </td>
  <td>{name}</td>
</tr>
<tr>
  <td>E: </td>
  <td>{email}</td>
</tr>
<tr>
  <td>P: </td>
  <td>{phone}</td>
</tr>
```

# <h1 align=center>10+ New Test Cases for Invitations Feature</h1>

---

### 1. **Test Invitation Creation Service**
**Description**: Verify that an invitation can be successfully created with a unique invite code and QR code.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/21">here</a>

#### Steps:
1. Call the `POST /invitations` endpoint with valid invitee details.
2. Verify:
   - The response status is `201 CREATED`.
   - The invite code and QR code URL are present in the response.
3. Assert that the QR code is stored in MinIO.

---

### 2. **Test QR Code Storage in MinIO**
**Description**: Ensure the generated QR code is correctly stored in the MinIO bucket.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/33">here</a>

#### Steps:
1. Create an invitation.
2. Retrieve the file from the MinIO bucket using the invite code as the filename.
3. Assert:
   - The file exists in the specified bucket.
   - The file format is valid (PNG).
   - The content matches the expected QR code data.

---

### 3. **Test Invitation Acceptance Service - Positive**
**Description**: Validate that an invitation can be accepted with a valid invite code and nickname.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/35">here</a>

#### Steps:
1. Create an invitation.
2. Call the `GET /accept` endpoint with the invite code and Base64-encoded nickname.
3. Verify:
   - The response redirects to the specified URL.
   - The invitation status is updated to "used."

---

### 4. **Test Resending Invitations Service - Positive**
**Description**: Verify that an invitation email can be resent.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/29">here</a>

#### Steps:
1. Create an invitation.
2. Call the `POST /invitations/{invite_code}/resend` endpoint.
3. Verify:
   - The response status is `200 OK`.
   - The QR code is regenerated and updated in MinIO.

---

### 5. **Test Invitation Updates Service**
**Description**: Ensure invitation details can be updated, such as the invitee's email or expiration date.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/27">here</a>

#### Steps:
1. Create an invitation.
2. Call the `PUT /invitations/{invite_code}` endpoint with updated details.
3. Verify:
   - The response status is `200 OK`.
   - The invitation record is updated in the database.
   - The QR code remains valid.

---

### 6. **Test Invitation Acceptance Service - Negative**
**Description**: Validate that an invitation can be decline with an invalid invite code and nickname.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/35">here</a>

#### Steps:
1. Create an invitation.
2. Call the `GET /accept` endpoint with the invalid invite code and Base64-encoded nickname.
3. Verify:
   - The response status is `400 Bad Request`.

---

### 7. **Test Deleting Invitations Service**
**Description**: Validate that an invitation can be deleted, and its QR code is removed from MinIO.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/31">here</a>

#### Steps:
1. Create an invitation.
2. Call the `DELETE /invitations/{invite_code}` endpoint.
3. Verify:
   - The response status is `204 No Content`.
   - The invitation record is removed from the database.
   - The QR code is deleted from the MinIO bucket.

---

### 8. **Test Listing Invitations by Code Service**
**Description**: Ensure that invitation details can be retrieved using the invite code.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/23">here</a>

#### Steps:
1. Create an invitation.
2. Call the `GET /invitations/{invite_code}` endpoint.
3. Verify:
   - The response status is `200 OK`.
   - The response contains accurate details (invite code, email, status, QR code URL).

---

### 9. **Test Listing All Invitations for a User Service**
**Description**: Verify that all invitations for a user can be retrieved, with pagination support.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/25">here</a>

#### Steps:
1. Create multiple invitations for a user.
2. Call the `GET /users/{user_id}/invitations` endpoint with pagination parameters.
3. Verify:
   - The response status is `200 OK`.
   - The response contains the correct number of invitations per page.
   - HATEOAS links (`next`, `prev`) are included in the response.

---

### 10. **Test Invitation Acceptance Router - Positive**
**Description**: Validate that an invitation can be accepted with a valid invite code and nickname.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/37">here</a>

#### Steps:
1. Create an invitation.
2. Call the `GET /accept` endpoint with the invite code and Base64-encoded nickname.
3. Verify:
   - The response redirects to the specified URL.
   - The invitation status is updated to "used."

---

### 11. **Test Invitation Acceptance Router - Negative**
**Description**: Validate that an invitation can be decline with an invalid invite code and nickname.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/37">here</a>

#### Steps:
1. Create an invitation.
2. Call the `GET /accept` endpoint with the invalid invite code and Base64-encoded nickname.
3. Verify:
   - The response status is `400 Bad Request`.

---

### 12. **Test Resending Invitations Service - Negative**
**Description**: Verify that an invitation email can be resent.
**Issue Link**: <a href="https://github.com/dylandacosta8/is601_final/issues/29">here</a>

#### Steps:
1. Create an invitation.
2. Call the `POST /invitations/{invite_code}/resend` endpoint with an invalid invite code
3. Verify:
   - The response status is `400 Bad Request`.
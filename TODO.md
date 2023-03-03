# What are we to do?

When you complete a task, please check it off. If you are unsure about a task, please ask.

Check it off like this example:

- [x] This is a completed task

- [ ] This is an incomplete task

## Tasks

- [ ] Endpoint to upload APK files with will return a unique id

- [ ] There should be user management system (Admin, Staff)

- [ ] Endpoint to create a new feedback request

    Feedback Model:

  - id
  - ticket_id
  - email
  - type (APK or Link)
  - link (could be null)
  - apk_id (could be null)
  - status (pending, active, completed)
  - assigned_to (assigned user) (could be null)
  - created_at
  - updated_at

- [ ] Endpoint to get all feedback requests (with pagination) (with sorting)

- [ ] Endpoint to get a feedback request by id

- [ ] Endpoint to close a feedback request

- [ ] Endpoint to self-assign a feedback request to the logged in user
  
  (if the feedback request is already assigned to someone else, it should return an error)
  (if the feedback request is already closed, it should return an error)
  (if the feedback request is already assigned to the logged in user, it should return an error)
  (when the feedback request is assigned to the logged in user, the status should be changed to active)

- [ ] Endpoint to unassign a feedback request from the logged in user

    (if the feedback request is already closed, it should return an error)
    (if the feedback request is not assigned to the logged in user, it should return an error)
    (when the feedback request is unassigned from the logged in user, the status should be changed to pending)

- [ ] Endpoint to get all feedback requests assigned to the logged in user (with pagination) (with sorting)

- [ ] Endpoint to add review to a feedback request

    Review Model:

  - id
  - feedback_id
  - comments (there could be one or more comments)
  - images (there could be one or more images)

  An idea would be to create a new table called `images` and store the images which will contain the following fields:

    Image Model:

  - id
  - image
  - review_id

  An idea would be to create a new table called `comments` and store the comments which will contain the following fields:

    Comment Model:

  - id
  - comment
  - review_id

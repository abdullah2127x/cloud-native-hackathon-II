(backend) PS D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend> uv run pytest -v
==================================== test session starts =====================================
platform win32 -- Python 3.12.5, pytest-9.0.2, pluggy-1.6.0 -- D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.12.1, asyncio-1.3.0, cov-7.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
collected 228 items                                                                           

tests/integration/test_auth_setup.py::TestBetterAuthMigration::test_user_table_exists PASSED [  0%]
tests/integration/test_auth_setup.py::TestBetterAuthMigration::test_user_table_has_required_columns PASSED [  0%]
tests/integration/test_auth_setup.py::TestBetterAuthMigration::test_user_table_email_has_unique_constraint PASSED [  1%]
tests/integration/test_auth_setup.py::TestBetterAuthMigration::test_user_id_is_primary_key PASSED [  1%]
tests/integration/test_auth_setup.py::TestBetterAuthMigration::test_database_connection_is_working PASSED [  2%]
tests/integration/test_auth_setup.py::TestBetterAuthMigration::test_can_insert_user_record PASSED [  2%]
tests/integration/test_auth_setup.py::TestBetterAuthMigration::test_duplicate_email_is_prevented PASSED [  3%]
tests/integration/test_auth_setup.py::TestBetterAuthMigration::test_can_query_users_by_email PASSED [  3%]
tests/integration/test_tags_api.py::test_api_get_tags_empty PASSED                      [  3%]
tests/integration/test_tags_api.py::test_api_get_tags_with_tasks PASSED                 [  4%]
tests/integration/test_tags_api.py::test_api_get_tags_case_insensitive_merge PASSED     [  4%]
tests/integration/test_tags_api.py::test_api_get_tags_different_users_isolated FAILED   [  5%]
tests/integration/test_tags_api.py::test_api_get_tags_sorted_alphabetically PASSED      [  5%]
tests/integration/test_tags_api.py::test_api_get_tags_with_special_characters PASSED    [  6%]
tests/integration/test_tasks_api_filter.py::test_api_filter_by_status_pending PASSED    [  6%]
tests/integration/test_tasks_api_filter.py::test_api_filter_by_status_completed PASSED  [  7%]
tests/integration/test_tasks_api_filter.py::test_api_filter_by_priority PASSED          [  7%]
tests/integration/test_tasks_api_filter.py::test_api_filter_by_tags FAILED              [  7%]
tests/integration/test_tasks_api_filter.py::test_api_filter_by_no_tags PASSED           [  8%]
tests/integration/test_tasks_api_filter.py::test_api_combined_filters FAILED            [  8%]
tests/integration/test_tasks_api_filter.py::test_api_filter_returns_correct_counts PASSED [  9%]
tests/integration/test_tasks_api_filter.py::test_api_filter_with_search PASSED          [  9%]
tests/integration/test_tasks_api_priority.py::test_create_task_with_priority PASSED     [ 10%]
tests/integration/test_tasks_api_priority.py::test_create_task_invalid_priority PASSED  [ 10%]
tests/integration/test_tasks_api_priority.py::test_get_todos_default_sort_by_priority PASSED [ 10%]
tests/integration/test_tasks_api_priority.py::test_update_task_priority PASSED          [ 11%]
tests/integration/test_tasks_api_priority.py::test_get_task_includes_priority PASSED    [ 11%]
tests/integration/test_tasks_api_search.py::test_api_search_by_title PASSED             [ 12%]
tests/integration/test_tasks_api_search.py::test_api_search_by_description PASSED       [ 12%]
tests/integration/test_tasks_api_search.py::test_api_search_case_insensitive PASSED     [ 13%]
tests/integration/test_tasks_api_search.py::test_api_search_partial_match PASSED        [ 13%]
tests/integration/test_tasks_api_search.py::test_api_search_no_results PASSED           [ 14%]
tests/integration/test_tasks_api_search.py::test_api_search_returns_counts PASSED       [ 14%]
tests/integration/test_tasks_api_search.py::test_api_search_across_title_and_description PASSED [ 14%]
tests/integration/test_tasks_api_search.py::test_api_search_with_special_characters PASSED [ 15%]
tests/integration/test_tasks_api_sort.py::test_api_sort_by_title_asc PASSED             [ 15%]
tests/integration/test_tasks_api_sort.py::test_api_sort_by_title_desc PASSED            [ 16%]
tests/integration/test_tasks_api_sort.py::test_api_sort_by_created_at_desc PASSED       [ 16%]
tests/integration/test_tasks_api_sort.py::test_api_sort_by_created_at_asc PASSED        [ 17%]
tests/integration/test_tasks_api_sort.py::test_api_sort_by_priority PASSED              [ 17%]
tests/integration/test_tasks_api_sort.py::test_api_sort_default_priority PASSED         [ 17%]
tests/integration/test_tasks_api_sort.py::test_api_sort_with_filters FAILED             [ 18%]
tests/integration/test_tasks_api_sort.py::test_api_sort_with_search PASSED              [ 18%]
tests/integration/test_tasks_api_tags.py::test_api_create_task_with_tags PASSED         [ 19%]
tests/integration/test_tasks_api_tags.py::test_api_create_task_with_duplicate_tags PASSED [ 19%]
tests/integration/test_tasks_api_tags.py::test_api_create_task_with_case_insensitive_tags PASSED [ 20%]
tests/integration/test_tasks_api_tags.py::test_api_update_task_with_tags PASSED         [ 20%]
tests/integration/test_tasks_api_tags.py::test_api_update_task_replace_all_tags PASSED  [ 21%]
tests/integration/test_tasks_api_tags.py::test_api_get_task_includes_tags PASSED        [ 21%]
tests/integration/test_tasks_api_tags.py::test_api_list_tasks_includes_tags PASSED      [ 21%]
tests/mcpserver/test_add_task.py::TestAddTaskParams::test_valid_params_with_description PASSED [ 22%]
tests/mcpserver/test_add_task.py::TestAddTaskParams::test_valid_params_without_description PASSED [ 22%]
tests/mcpserver/test_add_task.py::TestAddTaskParams::test_missing_user_id_validation PASSED [ 23%]
tests/mcpserver/test_add_task.py::TestAddTaskParams::test_missing_title_validation PASSED [ 23%]
tests/mcpserver/test_add_task.py::TestAddTaskParams::test_empty_title_validation PASSED [ 24%] 
tests/mcpserver/test_add_task.py::TestAddTaskParams::test_title_max_length_validation PASSED [ 24%]
tests/mcpserver/test_add_task.py::TestAddTaskParams::test_title_max_length_boundary PASSED [ 25%]
tests/mcpserver/test_add_task.py::TestAddTaskParams::test_description_max_length_validation PASSED [ 25%]
tests/mcpserver/test_add_task.py::TestAddTaskParams::test_description_max_length_boundary PASSED [ 25%]
tests/mcpserver/test_add_task.py::TestAddTaskResponse::test_valid_response PASSED       [ 26%] 
tests/mcpserver/test_add_task.py::TestAddTaskResponse::test_response_status_is_created PASSED [ 26%]
tests/mcpserver/test_add_task.py::TestAddTaskResponse::test_response_message_is_success PASSED [ 27%]
tests/mcpserver/test_add_task.py::TestAddTaskIntegration::test_task_creation_in_database PASSED [ 27%]
tests/mcpserver/test_add_task.py::TestAddTaskIntegration::test_task_isolation_by_user PASSED [ 28%]
tests/mcpserver/test_add_task.py::TestAddTaskIntegration::test_timestamps_set_automatically PASSED [ 28%]
tests/mcpserver/test_auth.py::TestVerifyJWTToken::test_valid_token_verification PASSED  [ 28%] 
tests/mcpserver/test_auth.py::TestVerifyJWTToken::test_invalid_token_rejection PASSED   [ 29%]
tests/mcpserver/test_auth.py::TestVerifyJWTToken::test_expired_token_rejection PASSED   [ 29%]
tests/mcpserver/test_auth.py::TestVerifyJWTToken::test_empty_token_rejection PASSED     [ 30%]
tests/mcpserver/test_auth.py::TestExtractUserID::test_user_id_extraction PASSED         [ 30%]
tests/mcpserver/test_auth.py::TestExtractUserID::test_missing_user_id_rejection PASSED  [ 31%]
tests/mcpserver/test_auth.py::TestExtractUserID::test_invalid_token_rejection PASSED    [ 31%]
tests/mcpserver/test_auth.py::TestExtractTokenFromHeader::test_valid_header_parsing PASSED [ 32%]
tests/mcpserver/test_auth.py::TestExtractTokenFromHeader::test_missing_header_rejection PASSED [ 32%]
tests/mcpserver/test_auth.py::TestExtractTokenFromHeader::test_invalid_header_format_rejection PASSED [ 32%]
tests/mcpserver/test_auth.py::TestExtractTokenFromHeader::test_missing_token_in_header_rejection PASSED [ 33%]
tests/mcpserver/test_auth.py::TestExtractTokenFromHeader::test_case_insensitive_bearer PASSED [ 33%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskParams::test_valid_params PASSED [ 34%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskParams::test_missing_user_id_validation PASSED [ 34%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskParams::test_empty_user_id_validation PASSED [ 35%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskParams::test_missing_task_id_validation PASSED [ 35%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskParams::test_valid_params_with_string_task_id PASSED [ 35%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskParams::test_valid_params_with_numeric_task_id PASSED [ 36%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskResponse::test_valid_response_completed PASSED [ 36%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskResponse::test_valid_response_uncompleted PASSED [ 37%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskIntegration::test_toggle_pending_to_completed PASSED [ 37%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskIntegration::test_toggle_completed_to_pending PASSED [ 38%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskIntegration::test_updated_at_timestamp_refreshed PASSED [ 38%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskIntegration::test_cannot_toggle_other_users_task PASSED [ 39%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskIntegration::test_toggle_nonexistent_task PASSED [ 39%]
tests/mcpserver/test_complete_task.py::TestCompleteTaskIntegration::test_toggle_task_affects_only_one_record PASSED [ 39%]
tests/mcpserver/test_delete_task.py::TestDeleteTaskParams::test_valid_params_with_string_id PASSED [ 40%]
tests/mcpserver/test_delete_task.py::TestDeleteTaskParams::test_valid_params_with_numeric_id PASSED [ 40%]
tests/mcpserver/test_delete_task.py::TestDeleteTaskParams::test_missing_user_id_validation PASSED [ 41%]
tests/mcpserver/test_delete_task.py::TestDeleteTaskParams::test_empty_user_id_validation PASSED [ 41%]
tests/mcpserver/test_delete_task.py::TestDeleteTaskParams::test_missing_task_id_validation PASSED [ 42%]
tests/mcpserver/test_delete_task.py::TestDeleteTaskResponse::test_valid_response PASSED [ 42%] 
tests/mcpserver/test_delete_task.py::TestDeleteTaskIntegration::test_successful_hard_delete PASSED [ 42%]
tests/mcpserver/test_delete_task.py::TestDeleteTaskIntegration::test_cannot_delete_other_users_task PASSED [ 43%]
tests/mcpserver/test_delete_task.py::TestDeleteTaskIntegration::test_delete_nonexistent_task PASSED [ 43%]
tests/mcpserver/test_delete_task.py::TestDeleteTaskIntegration::test_delete_affects_only_one_task PASSED [ 44%]
tests/mcpserver/test_delete_task.py::TestDeleteTaskIntegration::test_deleted_task_not_retrievable PASSED [ 44%]
tests/mcpserver/test_errors.py::TestMCPToolError::test_error_creation PASSED            [ 45%]
tests/mcpserver/test_errors.py::TestMCPToolError::test_error_to_mcp_response PASSED     [ 45%]
tests/mcpserver/test_errors.py::TestValidationError::test_validation_error_creation PASSED [ 46%]
tests/mcpserver/test_errors.py::TestValidationError::test_validation_error_response PASSED [ 46%]
tests/mcpserver/test_errors.py::TestNotFoundError::test_not_found_error_creation PASSED [ 46%]
tests/mcpserver/test_errors.py::TestUnauthorizedError::test_unauthorized_error_creation PASSED [ 47%]
tests/mcpserver/test_errors.py::TestUnauthorizedError::test_unauthorized_error_default_message PASSED [ 47%]
tests/mcpserver/test_errors.py::TestDatabaseError::test_database_error_creation PASSED  [ 48%]
tests/mcpserver/test_errors.py::TestSuccessResponse::test_success_response_without_structured_content PASSED [ 48%]
tests/mcpserver/test_errors.py::TestSuccessResponse::test_success_response_with_structured_content PASSED [ 49%]
tests/mcpserver/test_errors.py::TestSuccessResponse::test_success_response_format_compliance PASSED [ 49%]
tests/mcpserver/test_errors.py::TestErrorResponse::test_error_response_creation PASSED  [ 50%] 
tests/mcpserver/test_errors.py::TestErrorResponse::test_error_response_format_compliance PASSED [ 50%]
tests/mcpserver/test_integration.py::TestAddTaskMCPIntegration::test_add_task_via_mcp_protocol PASSED [ 50%]
tests/mcpserver/test_integration.py::TestAddTaskMCPIntegration::test_add_task_error_handling_via_mcp PASSED [ 51%]
tests/mcpserver/test_integration.py::TestAddTaskMCPIntegration::test_add_task_tool_discovery PASSED [ 51%]
tests/mcpserver/test_integration.py::TestAddTaskMCPIntegration::test_mcp_tool_not_found PASSED [ 52%]
tests/mcpserver/test_integration.py::TestAddTaskMCPIntegration::test_add_task_with_optional_description_omitted PASSED [ 52%]
tests/mcpserver/test_integration.py::TestAddTaskMCPIntegration::test_mcp_response_json_serializable PASSED [ 53%]
tests/mcpserver/test_integration.py::TestListTasksMCPIntegration::test_list_tasks_via_mcp_protocol PASSED [ 53%]
tests/mcpserver/test_integration.py::TestListTasksMCPIntegration::test_list_tasks_with_pending_filter PASSED [ 53%]
tests/mcpserver/test_integration.py::TestListTasksMCPIntegration::test_list_tasks_with_completed_filter PASSED [ 54%]
tests/mcpserver/test_integration.py::TestListTasksMCPIntegration::test_list_tasks_empty_for_new_user PASSED [ 54%]
tests/mcpserver/test_integration.py::TestListTasksMCPIntegration::test_list_tasks_sorted_descending PASSED [ 55%]
tests/mcpserver/test_integration.py::TestListTasksMCPIntegration::test_list_tasks_user_isolation PASSED [ 55%]
tests/mcpserver/test_integration.py::TestListTasksMCPIntegration::test_list_tasks_invalid_status PASSED [ 56%]
tests/mcpserver/test_integration.py::TestCompleteTaskMCPIntegration::test_complete_task_via_mcp_protocol PASSED [ 56%]
tests/mcpserver/test_integration.py::TestCompleteTaskMCPIntegration::test_toggle_task_to_completed PASSED [ 57%]
tests/mcpserver/test_integration.py::TestCompleteTaskMCPIntegration::test_toggle_task_to_uncompleted PASSED [ 57%]
tests/mcpserver/test_integration.py::TestCompleteTaskMCPIntegration::test_complete_task_nonexistent_task PASSED [ 57%]
tests/mcpserver/test_integration.py::TestCompleteTaskMCPIntegration::test_complete_task_user_isolation PASSED [ 58%]
tests/mcpserver/test_integration.py::TestCompleteTaskMCPIntegration::test_complete_task_invalid_task_id PASSED [ 58%]
tests/mcpserver/test_integration.py::TestCompleteTaskMCPIntegration::test_complete_task_tool_discovery PASSED [ 59%]
tests/mcpserver/test_integration.py::TestUpdateTaskMCPIntegration::test_update_task_via_mcp_protocol PASSED [ 59%]
tests/mcpserver/test_integration.py::TestUpdateTaskMCPIntegration::test_update_title_only PASSED [ 60%]
tests/mcpserver/test_integration.py::TestUpdateTaskMCPIntegration::test_update_description_only
 PASSED [ 60%]
tests/mcpserver/test_integration.py::TestUpdateTaskMCPIntegration::test_update_both_fields PASSED [ 60%]
tests/mcpserver/test_integration.py::TestUpdateTaskMCPIntegration::test_update_task_nonexistent
 PASSED [ 61%]
tests/mcpserver/test_integration.py::TestUpdateTaskMCPIntegration::test_update_task_user_isolation PASSED [ 61%]
tests/mcpserver/test_integration.py::TestUpdateTaskMCPIntegration::test_update_task_missing_both_fields PASSED [ 62%]
tests/mcpserver/test_integration.py::TestUpdateTaskMCPIntegration::test_update_task_tool_discovery PASSED [ 62%]
tests/mcpserver/test_integration.py::TestDeleteTaskMCPIntegration::test_delete_task_via_mcp_protocol PASSED [ 63%]
tests/mcpserver/test_integration.py::TestDeleteTaskMCPIntegration::test_successful_hard_delete PASSED [ 63%]
tests/mcpserver/test_integration.py::TestDeleteTaskMCPIntegration::test_delete_task_nonexistent
 PASSED [ 64%]
tests/mcpserver/test_integration.py::TestDeleteTaskMCPIntegration::test_delete_task_user_isolation PASSED [ 64%]
tests/mcpserver/test_integration.py::TestDeleteTaskMCPIntegration::test_delete_affects_only_one_task PASSED [ 64%]
tests/mcpserver/test_integration.py::TestDeleteTaskMCPIntegration::test_delete_task_confirmation_message PASSED [ 65%]
tests/mcpserver/test_integration.py::TestDeleteTaskMCPIntegration::test_delete_task_tool_discovery PASSED [ 65%]
tests/mcpserver/test_list_tasks.py::TestListTasksParams::test_valid_params_with_all_status PASSED [ 66%]
tests/mcpserver/test_list_tasks.py::TestListTasksParams::test_valid_params_with_pending_status PASSED [ 66%]
tests/mcpserver/test_list_tasks.py::TestListTasksParams::test_valid_params_with_completed_status PASSED [ 67%]
tests/mcpserver/test_list_tasks.py::TestListTasksParams::test_valid_params_default_status PASSED [ 67%]
tests/mcpserver/test_list_tasks.py::TestListTasksParams::test_missing_user_id_validation PASSED [ 67%]
tests/mcpserver/test_list_tasks.py::TestListTasksParams::test_empty_user_id_validation PASSED [ 68%]
tests/mcpserver/test_list_tasks.py::TestListTasksParams::test_invalid_status_validation PASSED [ 68%]
tests/mcpserver/test_list_tasks.py::TestListTasksResponse::test_valid_response_with_tasks PASSED [ 69%]
tests/mcpserver/test_list_tasks.py::TestListTasksResponse::test_valid_response_empty_list PASSED [ 69%]
tests/mcpserver/test_list_tasks.py::TestListTasksResponse::test_task_item_with_all_fields PASSED [ 70%]
tests/mcpserver/test_list_tasks.py::TestListTasksResponse::test_task_item_without_descriptionPPASSED [ 70%]
tests/mcpserver/test_list_tasks.py::TestListTasksIntegration::test_list_all_tasks_for_user PASSED [ 71%]
tests/mcpserver/test_list_tasks.py::TestListTasksIntegration::test_list_pending_tasks_only PASSED [ 71%]
tests/mcpserver/test_list_tasks.py::TestListTasksIntegration::test_list_completed_tasks_only PASSED [ 71%]
tests/mcpserver/test_list_tasks.py::TestListTasksIntegration::test_empty_task_list_for_user PASSED [ 72%]
tests/mcpserver/test_list_tasks.py::TestListTasksIntegration::test_tasks_sorted_by_created_at_descending PASSED [ 72%]
tests/mcpserver/test_list_tasks.py::TestListTasksIntegration::test_user_isolation_in_list PASSED [ 73%]
tests/mcpserver/test_update_task.py::TestUpdateTaskParams::test_valid_params_update_title_only PASSED [ 73%]
tests/mcpserver/test_update_task.py::TestUpdateTaskParams::test_valid_params_update_description_only PASSED [ 74%]
tests/mcpserver/test_update_task.py::TestUpdateTaskParams::test_valid_params_update_both PASSED [ 74%]
tests/mcpserver/test_update_task.py::TestUpdateTaskParams::test_missing_user_id_validation PASSED [ 75%]
tests/mcpserver/test_update_task.py::TestUpdateTaskParams::test_empty_user_id_validation PASSED [ 75%]
tests/mcpserver/test_update_task.py::TestUpdateTaskParams::test_missing_task_id_validation PASSED [ 75%]
tests/mcpserver/test_update_task.py::TestUpdateTaskParams::test_missing_both_fields_validation PASSED [ 76%]
tests/mcpserver/test_update_task.py::TestUpdateTaskParams::test_empty_title_validation PASSED [ 76%]
tests/mcpserver/test_update_task.py::TestUpdateTaskParams::test_title_exceeds_max_length PASSED [ 77%]
tests/mcpserver/test_update_task.py::TestUpdateTaskParams::test_description_exceeds_max_length PASSED [ 77%]
tests/mcpserver/test_update_task.py::TestUpdateTaskResponse::test_valid_response PASSED [ 78%] 
tests/mcpserver/test_update_task.py::TestUpdateTaskIntegration::test_update_title_only PASSED [ 78%]
tests/mcpserver/test_update_task.py::TestUpdateTaskIntegration::test_update_description_only PASSED [ 78%]
tests/mcpserver/test_update_task.py::TestUpdateTaskIntegration::test_update_both_fields PASSED [ 79%]
tests/mcpserver/test_update_task.py::TestUpdateTaskIntegration::test_cannot_update_other_users_task PASSED [ 79%]
tests/mcpserver/test_update_task.py::TestUpdateTaskIntegration::test_update_nonexistent_task PASSED [ 80%]
tests/mcpserver/test_update_task.py::TestUpdateTaskIntegration::test_update_preserves_created_at PASSED [ 80%]
tests/mcpserver/test_update_task.py::TestUpdateTaskIntegration::test_update_affects_only_one_task PASSED [ 81%]
tests/unit/test_tag_crud.py::test_get_or_create_tag_new PASSED                          [ 81%]
tests/unit/test_tag_crud.py::test_get_or_create_tag_existing PASSED                     [ 82%]
tests/unit/test_tag_crud.py::test_list_tags PASSED                                      [ 82%]
tests/unit/test_tag_crud.py::test_get_tag_stats PASSED                                  [ 82%]
tests/unit/test_tag_crud.py::test_get_tags_for_task PASSED                              [ 83%]
tests/unit/test_task_crud_filter.py::test_list_tasks_with_status_filter_pending PASSED  [ 83%]
tests/unit/test_task_crud_filter.py::test_list_tasks_with_status_filter_completed PASSED [ 84%]
tests/unit/test_task_crud_filter.py::test_list_tasks_with_status_filter_all PASSED      [ 84%]
tests/unit/test_task_crud_filter.py::test_list_tasks_with_priority_filter PASSED        [ 85%]
tests/unit/test_task_crud_filter.py::test_list_tasks_with_tags_filter PASSED            [ 85%]
tests/unit/test_task_crud_filter.py::test_list_tasks_with_no_tags_filter PASSED         [ 85%]
tests/unit/test_task_crud_filter.py::test_list_tasks_with_combined_filters PASSED       [ 86%]
tests/unit/test_task_crud_priority.py::test_create_task_with_priority PASSED            [ 86%]
tests/unit/test_task_crud_priority.py::test_create_task_default_priority PASSED         [ 87%]
tests/unit/test_task_crud_priority.py::test_update_task_priority PASSED                 [ 87%]
tests/unit/test_task_crud_priority.py::test_list_tasks_sorted_by_priority PASSED        [ 88%]
tests/unit/test_task_crud_priority.py::test_list_tasks_priority_isolation PASSED        [ 88%]
tests/unit/test_task_crud_search.py::test_list_tasks_with_search_title PASSED           [ 89%]
tests/unit/test_task_crud_search.py::test_list_tasks_with_search_case_insensitive PASSED [ 89%]
tests/unit/test_task_crud_search.py::test_list_tasks_with_search_partial_match PASSED   [ 89%]
tests/unit/test_task_crud_search.py::test_list_tasks_with_search_no_results PASSED      [ 90%]
tests/unit/test_task_crud_search.py::test_list_tasks_with_search_across_title_and_description PASSED [ 90%]
tests/unit/test_task_crud_sort.py::test_list_tasks_with_title_sort_asc PASSED           [ 91%]
tests/unit/test_task_crud_sort.py::test_list_tasks_with_title_sort_desc PASSED          [ 91%]
tests/unit/test_task_crud_sort.py::test_list_tasks_with_created_at_sort_desc PASSED     [ 92%]
tests/unit/test_task_crud_sort.py::test_list_tasks_with_created_at_sort_asc PASSED      [ 92%]
tests/unit/test_task_crud_sort.py::test_list_tasks_with_priority_sort PASSED            [ 92%]
tests/unit/test_task_crud_sort.py::test_list_tasks_default_sort_priority PASSED         [ 93%]
tests/unit/test_task_crud_tags.py::test_create_task_with_tags PASSED                    [ 93%]
tests/unit/test_task_crud_tags.py::test_create_task_with_duplicate_tags PASSED          [ 94%]
tests/unit/test_task_crud_tags.py::test_update_task_with_tags PASSED                    [ 94%]
tests/unit/test_task_crud_tags.py::test_update_task_replace_all_tags PASSED             [ 95%]
tests/unit/test_task_crud_tags.py::test_create_task_with_case_insensitive_tags PASSED   [ 95%]
tests/unit/test_user_model.py::TestUserModel::test_create_user_with_all_fields PASSED   [ 96%] 
tests/unit/test_user_model.py::TestUserModel::test_user_email_is_unique_field PASSED    [ 96%] 
tests/unit/test_user_model.py::TestUserModel::test_user_email_verified_defaults_to_false PASSED [ 96%]
tests/unit/test_user_model.py::TestUserModel::test_user_has_primary_key PASSED          [ 97%]
tests/unit/test_user_model.py::TestUserModel::test_user_timestamps_are_set PASSED       [ 97%]
tests/unit/test_user_model.py::TestUserModel::test_user_model_has_all_required_fields PASSED [ 98%]
tests/unit/test_user_model.py::TestUserModel::test_user_model_table_name PASSED         [ 98%]
tests/unit/test_user_model.py::TestUserModel::test_user_accepts_valid_email_formats[valid@example.com] PASSED [ 99%]
tests/unit/test_user_model.py::TestUserModel::test_user_accepts_valid_email_formats[user.name@domain.co.uk] PASSED [ 99%]
tests/unit/test_user_model.py::TestUserModel::test_user_accepts_valid_email_formats[test+tag@subdomain.example.com] PASSED [100%]

========================================== FAILURES ========================================== 
_________________________ test_api_get_tags_different_users_isolated _________________________ 

client = <starlette.testclient.TestClient object at 0x0000024B60695D00>
auth_headers = {'Authorization': 'Bearer mock-token'}, mock_auth = None

    def test_api_get_tags_different_users_isolated(client, auth_headers, mock_auth):
        """Test GET /api/tags returns only tags for the authenticated user"""
        # Create task with tags for current user
        client.post(
            "/api/todos",
            json={
                "title": "User's work task",
                "tags": ["work", "urgent"]
            },
            headers=auth_headers
        )

        # Mock a different user
>       mock_auth.return_value = {"sub": "other-user-id"}
        ^^^^^^^^^^^^^^^^^^^^^^
E       AttributeError: 'NoneType' object has no attribute 'return_value'

tests\integration\test_tags_api.py:107: AttributeError
__________________________________ test_api_filter_by_tags ___________________________________ 

client = <starlette.testclient.TestClient object at 0x0000024B60675DC0>
auth_headers = {'Authorization': 'Bearer mock-token'}

    def test_api_filter_by_tags(client, auth_headers):
        """Test GET /api/todos with tags filter"""
        # Create tasks with different tags
        client.post("/api/todos", json={"title": "Work task", "tags": ["work", "urgent"]}, headers=auth_headers)
        client.post("/api/todos", json={"title": "Personal task", "tags": ["personal"]}, headers=auth_headers)
        client.post("/api/todos", json={"title": "Home task", "tags": ["home", "personal"]}, headers=auth_headers)

        # Filter for tasks with "work" tag
        response = client.get("/api/todos?tags=work", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
>       assert data["filtered"] == 1
E       assert 3 == 1

tests\integration\test_tasks_api_filter.py:76: AssertionError
_________________________________ test_api_combined_filters __________________________________ 

client = <starlette.testclient.TestClient object at 0x0000024B606CEA20>
auth_headers = {'Authorization': 'Bearer mock-token'}

    def test_api_combined_filters(client, auth_headers):
        """Test GET /api/todos with combined filters (AND logic)"""
        # Create tasks with different combinations
        client.post("/api/todos", json={
            "title": "High priority work",
            "priority": "high",
            "tags": ["work"],
            "completed": False
        }, headers=auth_headers)

        client.post("/api/todos", json={
            "title": "Low priority work",
            "priority": "low",
            "tags": ["work"],
            "completed": False
        }, headers=auth_headers)

        client.post("/api/todos", json={
            "title": "High priority personal",
            "priority": "high",
            "tags": ["personal"],
            "completed": False
        }, headers=auth_headers)

        client.post("/api/todos", json={
            "title": "High priority completed",
            "priority": "high",
            "tags": ["work"],
            "completed": True
        }, headers=auth_headers)

        # Filter for high priority AND work tag AND pending
        response = client.get("/api/todos?priority=high&tags=work&status=pending", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
>       assert data["filtered"] == 1
E       assert 2 == 1

tests\integration\test_tasks_api_filter.py:144: AssertionError
_________________________________ test_api_sort_with_filters _________________________________ 

client = <starlette.testclient.TestClient object at 0x0000024B608BDCA0>
auth_headers = {'Authorization': 'Bearer mock-token'}

    def test_api_sort_with_filters(client, auth_headers):
        """Test that sort works together with filters"""
        # Create tasks with different attributes
        client.post("/api/todos", json={
            "title": "High priority work",
            "priority": "high",
            "tags": ["work"],
            "completed": False
        }, headers=auth_headers)

        client.post("/api/todos", json={
            "title": "Low priority work",
            "priority": "low",
            "tags": ["work"],
            "completed": False
        }, headers=auth_headers)

        client.post("/api/todos", json={
            "title": "High priority personal",
            "priority": "high",
            "tags": ["personal"],
            "completed": False
        }, headers=auth_headers)

        # Filter by work tag and sort by priority
        response = client.get("/api/todos?tags=work&sort=priority&order=asc", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
>       assert data["filtered"] == 2  # Should return 2 work tasks
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       assert 3 == 2

tests\integration\test_tasks_api_sort.py:133: AssertionError
====================================== warnings summary ====================================== 
.venv\Lib\site-packages\sqlmodel\main.py:534
  D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\sqlmodel\main.py:534: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    new_cls = super().__new__(cls, name, bases, dict_used, **config_kwargs)

src\config.py:8
  D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\config.py:8: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

src\schemas\task.py:94
  D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\schemas\task.py:94: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class TaskRead(BaseModel):

tests/integration/test_tags_api.py::test_api_get_tags_empty
  D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\main.py:53: DeprecationWarning:
          on_event is deprecated, use lifespan event handlers instead.

          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).   

    @app.on_event("startup")

tests/integration/test_tags_api.py::test_api_get_tags_empty
tests/integration/test_tags_api.py::test_api_get_tags_empty
  D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\.venv\Lib\site-packages\fastapi\applications.py:4576: DeprecationWarning:
          on_event is deprecated, use lifespan event handlers instead.

          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).   

    return self.router.on_event(event_type)

tests/integration/test_tags_api.py::test_api_get_tags_empty
  D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\src\main.py:62: DeprecationWarning:
          on_event is deprecated, use lifespan event handlers instead.

          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).   

    @app.on_event("shutdown")

tests/mcpserver/test_integration.py: 5398 warnings
  D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend\mcpserver\logging_config.py:15: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    "timestamp": datetime.utcnow().isoformat() + "Z",

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================================= tests coverage ======================================= 
______________________ coverage: platform win32, python 3.12.5-final-0 _______________________ 

Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
src\__init__.py                       0      0   100%
src\auth\__init__.py                  0      0   100%
src\auth\dependencies.py             16     10    38%   27-46
src\auth\jwt_handler.py              31     21    32%   31-56, 72-78
src\config.py                        32      5    84%   34-37, 46
src\crud\__init__.py                  0      0   100%
src\crud\tag.py                      52     17    67%   59-68, 112, 169-189
src\crud\task.py                    116     19    84%   89-95, 120, 149, 232, 274, 276, 278, 316-318, 336-343
src\db\__init__.py                    0      0   100%
src\db\database.py                   25      6    76%   18, 44-46, 51-52
src\exceptions\base.py               17      7    59%   12-13, 19, 25-26, 32-33
src\exceptions\handlers.py           14      6    57%   13, 21, 29-32
src\main.py                          33      1    97%   71
src\middleware\cors.py                5      0   100%
src\middleware\error_handler.py      18     10    44%   15-35
src\middleware\logging.py            11      0   100%
src\models\__init__.py                0      0   100%
src\models\priority.py                7      0   100%
src\models\tag.py                    18      0   100%
src\models\task.py                   21      0   100%
src\models\user.py                   13      0   100%
src\routers\__init__.py               0      0   100%
src\routers\health.py                 9      1    89%   18
src\routers\tags.py                  13      0   100%
src\routers\tasks.py                 57      5    91%   85-86, 133, 143-144
src\schemas\__init__.py               0      0   100%
src\schemas\task.py                  96      9    91%   56, 58, 60, 79, 84, 86, 88, 114, 118   
---------------------------------------------------------------
TOTAL                               604    117    81%
Coverage HTML written to dir htmlcov
Required test coverage of 70% reached. Total coverage: 80.63%
================================== short test summary info =================================== 
FAILED tests/integration/test_tags_api.py::test_api_get_tags_different_users_isolated - AttributeError: 'NoneType' object has no attribute 'return_value'
FAILED tests/integration/test_tasks_api_filter.py::test_api_filter_by_tags - assert 3 == 1     
FAILED tests/integration/test_tasks_api_filter.py::test_api_combined_filters - assert 2 == 1   
FAILED tests/integration/test_tasks_api_sort.py::test_api_sort_with_filters - assert 3 == 2    
================== 4 failed, 224 passed, 5405 warnings in 106.80s (0:01:46) ================== 
(backend) PS D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\backend>
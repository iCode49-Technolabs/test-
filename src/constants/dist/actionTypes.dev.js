"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.RECORDEVIDENCE = exports.PROGRESSDATA = exports.LESSONPLAN = exports.VIEWKEYOUTCOME = exports.STRATEGIESADJUSTMENT = exports.KEY_OUTCOME_ID = exports.FILESTATUS = exports.SHARE_SCHOOL = exports.SOFT_SKILL_ROOT_CAUSE = exports.SOFT_SKILL_SUB_CATEGORY = exports.OVERDUEREVIEWCOUNT = exports.UPCOMINGREVIEWCOUNT = exports.ALLREVIEWCOUNT = exports.BARGRAPHCOUNTS = exports.STUDENTCONVODATA = exports.ORGANISE_FORMAL_ASSESSMENT = exports.DOCUMENT_REPOSITRY = exports.REVIEW_PAST_IEP = exports.LESSON_UNIT = exports.MODIFICATIONSTUDENT = exports.TEACHERASSESSMENTREQUEST = exports.VIEWALLREVIEW = exports.OVERDUEREVIEWS = exports.UPCOMINGREVIEWS = exports.STUDENT_PROFILE = exports.USER_PROFILE_DATA = exports.TEACHER_FORM = exports.NEGOTIATE_GOAL = exports.NEW_STUDENT_DURATION = exports.VIEW_CATEGORY_OF_CONCERN = exports.VIEW_REVIEW = exports.VIEW_SOFT_SKILL = exports.VIEW_STRATERGIES_ADJUSTMENTS = exports.KEY_OUTCOME = exports.IEP_STEP3 = exports.IEP_STEP2 = exports.IEPID = exports.VIEW_SUBJECT = exports.NEWSTUDENTDETAILS = exports.TEACHERCOMMENTS = exports.MAPSTUDENTVIEWS = exports.ASSESSMENT_TYPE = exports.IEP_STEP_1_PERSONALINFO = exports.IEP_STEP_1_IMPINFO = exports.IEP_STEP_1_STUDENTDETAILS = exports.POPULATEYEARLEVELS = exports.YEARLEVELDATA = exports.SUPPORTSTAFF = exports.STUDENT = exports.COORDINATOR = exports.ASSIGNTEACHERCOORDINATOR = exports.TEACHERTAGGING = exports.STUDENTSVOICCHOICE = exports.FORGOTPASSWORD = exports.TEACHERNAMES = exports.PARENT = exports.TEACHER = exports.ACTIVESTUDENT = exports.TOTALSTUDENT = exports.STUDENTDETAILS = exports.SCHOOLONBOARDING = exports.STUDENTASSESSMENTCOUNT = exports.CURRICULUM = exports.NEWSTUDENTCOUNT = exports.SCHOOLSDETAILS = exports.COORDINATORSCOUNT = exports.TEACHERSCOUNT = exports.STUDENTSCOUNT = exports.USERSCOUNT = exports.SCHOOLSCOUNT = exports.SCHOOLS = exports.ROLES = exports.VALIDATE = exports.LOGOUT = exports.LOGIN = exports.AUTH = void 0;
var AUTH = 'AUTH';
exports.AUTH = AUTH;
var LOGIN = 'LOGOIN';
exports.LOGIN = LOGIN;
var LOGOUT = 'LOGOUT';
exports.LOGOUT = LOGOUT;
var VALIDATE = 'VALIDATE';
exports.VALIDATE = VALIDATE;
var ROLES = 'ROLES';
exports.ROLES = ROLES;
var SCHOOLS = 'SCHOOLS';
exports.SCHOOLS = SCHOOLS;
var SCHOOLSCOUNT = 'SCHOOLSCOUNT';
exports.SCHOOLSCOUNT = SCHOOLSCOUNT;
var USERSCOUNT = 'USERSCOUNT';
exports.USERSCOUNT = USERSCOUNT;
var STUDENTSCOUNT = 'STUDENTSCOUNT';
exports.STUDENTSCOUNT = STUDENTSCOUNT;
var TEACHERSCOUNT = 'TEACHERSCOUNT';
exports.TEACHERSCOUNT = TEACHERSCOUNT;
var COORDINATORSCOUNT = 'COORDINATORSCOUNT';
exports.COORDINATORSCOUNT = COORDINATORSCOUNT;
var SCHOOLSDETAILS = 'SCHOOLSDETAILS';
exports.SCHOOLSDETAILS = SCHOOLSDETAILS;
var NEWSTUDENTCOUNT = 'NEWSTUDENTCOUNT';
exports.NEWSTUDENTCOUNT = NEWSTUDENTCOUNT;
var CURRICULUM = 'CURRICULUM';
exports.CURRICULUM = CURRICULUM;
var STUDENTASSESSMENTCOUNT = 'STUDENTASSESSMENTCOUNT';
exports.STUDENTASSESSMENTCOUNT = STUDENTASSESSMENTCOUNT;
var SCHOOLONBOARDING = 'SCHOOLONBOARDING';
exports.SCHOOLONBOARDING = SCHOOLONBOARDING;
var STUDENTDETAILS = 'STUDENTDETAILS';
exports.STUDENTDETAILS = STUDENTDETAILS;
var TOTALSTUDENT = 'TOTALSTUDENT';
exports.TOTALSTUDENT = TOTALSTUDENT;
var ACTIVESTUDENT = 'ACTIVESTUDENT';
exports.ACTIVESTUDENT = ACTIVESTUDENT;
var TEACHER = 'TEACHER';
exports.TEACHER = TEACHER;
var PARENT = 'PARENT';
exports.PARENT = PARENT;
var TEACHERNAMES = 'TEACHERNAMEST';
exports.TEACHERNAMES = TEACHERNAMES;
var FORGOTPASSWORD = 'FORGOTPASSWORD';
exports.FORGOTPASSWORD = FORGOTPASSWORD;
var STUDENTSVOICCHOICE = 'STUDENTSVOICCHOICE';
exports.STUDENTSVOICCHOICE = STUDENTSVOICCHOICE;
var TEACHERTAGGING = 'TEACHERTAGGING';
exports.TEACHERTAGGING = TEACHERTAGGING;
var ASSIGNTEACHERCOORDINATOR = 'ASSIGNTEACHERCOORDINATOR';
exports.ASSIGNTEACHERCOORDINATOR = ASSIGNTEACHERCOORDINATOR;
var COORDINATOR = 'COORDINATOR';
exports.COORDINATOR = COORDINATOR;
var STUDENT = 'STUDENT';
exports.STUDENT = STUDENT;
var SUPPORTSTAFF = 'SUPPORTSTAFF';
exports.SUPPORTSTAFF = SUPPORTSTAFF;
var YEARLEVELDATA = 'YEARLEVELDATA';
exports.YEARLEVELDATA = YEARLEVELDATA;
var POPULATEYEARLEVELS = 'POPULATEYEARLEVELS';
exports.POPULATEYEARLEVELS = POPULATEYEARLEVELS;
var IEP_STEP_1_STUDENTDETAILS = 'IEP_STEP_1_STUDENTDETAILS';
exports.IEP_STEP_1_STUDENTDETAILS = IEP_STEP_1_STUDENTDETAILS;
var IEP_STEP_1_IMPINFO = 'IEP_STEP_1_IMPINFO';
exports.IEP_STEP_1_IMPINFO = IEP_STEP_1_IMPINFO;
var IEP_STEP_1_PERSONALINFO = 'IEP_STEP_1_PERSONALINFO';
exports.IEP_STEP_1_PERSONALINFO = IEP_STEP_1_PERSONALINFO;
var ASSESSMENT_TYPE = 'ASSESSMENT_TYPE';
exports.ASSESSMENT_TYPE = ASSESSMENT_TYPE;
var MAPSTUDENTVIEWS = 'MAPSTUDENTVIEWS';
exports.MAPSTUDENTVIEWS = MAPSTUDENTVIEWS;
var TEACHERCOMMENTS = 'TEACHERCOMMENTS';
exports.TEACHERCOMMENTS = TEACHERCOMMENTS;
var NEWSTUDENTDETAILS = 'NEWSTUDENTDETAILS';
exports.NEWSTUDENTDETAILS = NEWSTUDENTDETAILS;
var VIEW_SUBJECT = 'VIEW_SUBJECT';
exports.VIEW_SUBJECT = VIEW_SUBJECT;
var IEPID = 'IEPID';
exports.IEPID = IEPID;
var IEP_STEP2 = 'IEP_STEP2';
exports.IEP_STEP2 = IEP_STEP2;
var IEP_STEP3 = 'IEP_STEP3';
exports.IEP_STEP3 = IEP_STEP3;
var KEY_OUTCOME = 'KEY_OUTCOME';
exports.KEY_OUTCOME = KEY_OUTCOME;
var VIEW_STRATERGIES_ADJUSTMENTS = 'VIEW_STRATERGIES_ADJUSTMENTS';
exports.VIEW_STRATERGIES_ADJUSTMENTS = VIEW_STRATERGIES_ADJUSTMENTS;
var VIEW_SOFT_SKILL = 'VIEW_SOFT_SKILL';
exports.VIEW_SOFT_SKILL = VIEW_SOFT_SKILL;
var VIEW_REVIEW = 'VIEW_REVIEW';
exports.VIEW_REVIEW = VIEW_REVIEW;
var VIEW_CATEGORY_OF_CONCERN = 'VIEW_CATEGORY_OF_CONCERN';
exports.VIEW_CATEGORY_OF_CONCERN = VIEW_CATEGORY_OF_CONCERN;
var NEW_STUDENT_DURATION = 'NEW_STUDENT_DURATION';
exports.NEW_STUDENT_DURATION = NEW_STUDENT_DURATION;
var NEGOTIATE_GOAL = 'NEGOTIATE_GOAL';
exports.NEGOTIATE_GOAL = NEGOTIATE_GOAL;
var TEACHER_FORM = 'TEACHER_FORM';
exports.TEACHER_FORM = TEACHER_FORM;
var USER_PROFILE_DATA = 'USER_PROFILE_DATA';
exports.USER_PROFILE_DATA = USER_PROFILE_DATA;
var STUDENT_PROFILE = 'STUDENT_PROFILE';
exports.STUDENT_PROFILE = STUDENT_PROFILE;
var UPCOMINGREVIEWS = 'UPCOMINGREVIEWS';
exports.UPCOMINGREVIEWS = UPCOMINGREVIEWS;
var OVERDUEREVIEWS = 'OVERDUEREVIEWS';
exports.OVERDUEREVIEWS = OVERDUEREVIEWS;
var VIEWALLREVIEW = 'VIEWALLREVIEW';
exports.VIEWALLREVIEW = VIEWALLREVIEW;
var TEACHERASSESSMENTREQUEST = 'TEACHERASSESSMENTREQUEST';
exports.TEACHERASSESSMENTREQUEST = TEACHERASSESSMENTREQUEST;
var MODIFICATIONSTUDENT = 'MODIFICATIONSTUDENT';
exports.MODIFICATIONSTUDENT = MODIFICATIONSTUDENT;
var LESSON_UNIT = 'LESSON_UNIT';
exports.LESSON_UNIT = LESSON_UNIT;
var REVIEW_PAST_IEP = 'REVIEW_PAST_IEP';
exports.REVIEW_PAST_IEP = REVIEW_PAST_IEP;
var DOCUMENT_REPOSITRY = 'DOCUMENT_REPOSITRY';
exports.DOCUMENT_REPOSITRY = DOCUMENT_REPOSITRY;
var ORGANISE_FORMAL_ASSESSMENT = "ORGANISE_FORMAL_ASSESSMENT";
exports.ORGANISE_FORMAL_ASSESSMENT = ORGANISE_FORMAL_ASSESSMENT;
var STUDENTCONVODATA = "STUDENTCONVODATA";
exports.STUDENTCONVODATA = STUDENTCONVODATA;
var BARGRAPHCOUNTS = "BARGRAPHCOUNTS";
exports.BARGRAPHCOUNTS = BARGRAPHCOUNTS;
var ALLREVIEWCOUNT = "ALLREVIEWCOUNT";
exports.ALLREVIEWCOUNT = ALLREVIEWCOUNT;
var UPCOMINGREVIEWCOUNT = "UPCOMINGREVIEWCOUNT";
exports.UPCOMINGREVIEWCOUNT = UPCOMINGREVIEWCOUNT;
var OVERDUEREVIEWCOUNT = "OVERDUEREVIEWCOUNT";
exports.OVERDUEREVIEWCOUNT = OVERDUEREVIEWCOUNT;
var SOFT_SKILL_SUB_CATEGORY = "SOFT_SKILL_SUB_CATEGORY";
exports.SOFT_SKILL_SUB_CATEGORY = SOFT_SKILL_SUB_CATEGORY;
var SOFT_SKILL_ROOT_CAUSE = "SOFT_SKILL_ROOT_CAUSE";
exports.SOFT_SKILL_ROOT_CAUSE = SOFT_SKILL_ROOT_CAUSE;
var SHARE_SCHOOL = "SHARE_SCHOOL";
exports.SHARE_SCHOOL = SHARE_SCHOOL;
var FILESTATUS = "FILESTATUS";
exports.FILESTATUS = FILESTATUS;
var KEY_OUTCOME_ID = "KEY_OUTCOME_ID";
exports.KEY_OUTCOME_ID = KEY_OUTCOME_ID;
var STRATEGIESADJUSTMENT = "STRATEGIESADJUSTMENT";
exports.STRATEGIESADJUSTMENT = STRATEGIESADJUSTMENT;
var VIEWKEYOUTCOME = "VIEWKEYOUTCOME";
exports.VIEWKEYOUTCOME = VIEWKEYOUTCOME;
var LESSONPLAN = "LESSONPLAN";
exports.LESSONPLAN = LESSONPLAN;
var PROGRESSDATA = "PROGRESSDATA";
exports.PROGRESSDATA = PROGRESSDATA;
var RECORDEVIDENCE = "RECORDEVIDENCE";
exports.RECORDEVIDENCE = RECORDEVIDENCE;
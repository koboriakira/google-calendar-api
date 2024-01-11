#!/usr/bin/env node
/** @format */

import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { GoogleCalendarApi } from "../lib/google_calendar_api";

const app = new cdk.App();
new GoogleCalendarApi(app, "GoogleCalendarApi", {});

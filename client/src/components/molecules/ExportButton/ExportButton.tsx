import React from 'react';
import { DownloadOutlined } from '@ant-design/icons';
import { Button } from 'antd';
import { exportFileUrl } from '../../../api/merger';

export const ExportButton = () => (
	<Button icon={<DownloadOutlined />} href={exportFileUrl}>
		Export
	</Button>
);

# coding: utf8


def extract_slices(preprocessed_T1, slice_direction=0, slice_mode='original'):
    """
    This function extracts the slices from three directions
    :param preprocessed_T1:
    :param slice_direction: which axis direction that the slices were extracted
    :return:
    """
    import torch
    import os

    image_tensor = torch.load(preprocessed_T1)
    # reshape the tensor, delete the first dimension for slice-level
    image_tensor = image_tensor.view(image_tensor.shape[1], image_tensor.shape[2], image_tensor.shape[3])

    # sagital
    slice_list_sag = range(20, image_tensor.shape[0] - 20)  # delete the first 20 slice and last 20 slices

    basedir = os.getcwd()
    output_file_original = []
    output_file_rgb = []
    if slice_direction == 0:
        for index_slice, index_slice_list in zip(slice_list_sag, range(len(slice_list_sag))):
            # for i in slice_list:
            # sagital
            slice_select_sag = image_tensor[index_slice, :, :]

            # convert the slices to images based on if transfer learning or not
            # train from scratch
            extracted_slice_original_sag = slice_select_sag.unsqueeze(0)  # shape should be 1 * W * L

            # train for transfer learning, creating the fake RGB image.
            slice_select_sag = (slice_select_sag - slice_select_sag.min()) / (slice_select_sag.max() - slice_select_sag.min())
            extracted_slice_rgb_sag = torch.stack((slice_select_sag, slice_select_sag, slice_select_sag))  # shape should be 3 * W * L

            # save into .pt format
            if slice_mode == 'original':
                output_file_original.append(
                        os.path.join(
                            basedir,
                            os.path.basename(preprocessed_T1).split('.pt')[0]
                            + '_axis-sag_originalslice-'
                            + str(index_slice)
                            + '.pt'
                            )
                        )
                torch.save(extracted_slice_original_sag.clone(), output_file_original[index_slice_list])
            elif slice_mode == 'rgb':
                output_file_rgb.append(
                        os.path.join(
                            basedir,
                            os.path.basename(preprocessed_T1).split('.pt')[0]
                            + '_axis-sag_rgbslice-'
                            + str(index_slice)
                            + '.pt'
                            )
                        )
                torch.save(extracted_slice_rgb_sag.clone(), output_file_rgb[index_slice_list])

    elif slice_direction == 1:
        # cornal
        slice_list_cor = range(15, image_tensor.shape[1] - 15)  # delete the first 20 slice and last 15 slices
        for index_slice, index_slice_list in zip(slice_list_cor, range(len(slice_list_cor))):
            # for i in slice_list:
            # sagital
            slice_select_cor = image_tensor[:, index_slice, :]

            # convert the slices to images based on if transfer learning or not
            # train from scratch
            extracted_slice_original_cor = slice_select_cor.unsqueeze(0)  # shape should be 1 * W * L

            # train for transfer learning, creating the fake RGB image.
            slice_select_cor = (slice_select_cor - slice_select_cor.min()) / (slice_select_cor.max() - slice_select_cor.min())
            extracted_slice_rgb_cor = torch.stack((slice_select_cor, slice_select_cor, slice_select_cor))  # shape should be 3 * W * L

            # save into .pt format
            if slice_mode == 'original':
                output_file_original.append(
                        os.path.join(
                            basedir,
                            os.path.basename(preprocessed_T1).split('.pt')[0]
                            + '_axis-cor_originalslice-'
                            + str(index_slice)
                            + '.pt')
                        )
                torch.save(extracted_slice_original_cor.clone(), output_file_original[index_slice_list])
            elif slice_mode == 'rgb':
                output_file_rgb.append(
                    os.path.join(
                        basedir,
                        os.path.basename(preprocessed_T1).split('.pt')[0]
                        + '_axis-cor_rgbslice-'
                        + str(index_slice)
                        + '.pt'
                        )
                    )
                torch.save(extracted_slice_rgb_cor.clone(), output_file_rgb[index_slice_list])

    else:

        # axial
        slice_list_axi = range(15, image_tensor.shape[2] - 15)  # delete the first 20 slice and last 15 slices
        for index_slice, index_slice_list in zip(slice_list_axi, range(len(slice_list_axi))):
            # for i in slice_list:
            # sagital
            slice_select_axi = image_tensor[:, :, index_slice]

            # convert the slices to images based on if transfer learning or not
            # train from scratch
            extracted_slice_original_axi = slice_select_axi.unsqueeze(0)  # shape should be 1 * W * L

            # train for transfer learning, creating the fake RGB image.
            slice_select_axi = (slice_select_axi - slice_select_axi.min()) / (slice_select_axi.max() - slice_select_axi.min())
            extracted_slice_rgb_axi = torch.stack((slice_select_axi, slice_select_axi, slice_select_axi))  # shape should be 3 * W * L

            # save into .pt format
            if slice_mode == 'original':
                output_file_original.append(
                        os.path.join(
                            basedir,
                            os.path.basename(preprocessed_T1).split('.pt')[0]
                            + '_axis-axi_originalslice-'
                            + str(index_slice)
                            + '.pt'
                            )
                        )
                torch.save(extracted_slice_original_axi.clone(), output_file_original[index_slice_list])
            elif slice_mode == 'rgb':
                output_file_rgb.append(
                        os.path.join(
                            basedir,
                            os.path.basename(preprocessed_T1).split('.pt')[0]
                            + '_axis-axi_rgbslice-'
                            + str(index_slice)
                            + '.pt'
                            )
                        )
                torch.save(extracted_slice_rgb_axi.clone(), output_file_rgb[index_slice_list])

    return output_file_rgb, output_file_original


def extract_patches(preprocessed_T1, patch_size, stride_size):
    """
    This function extracts the patches from three directions
    :param preprocessed_T1:
    :return:
    """
    import torch
    import os

    basedir = os.getcwd()
    image_tensor = torch.load(preprocessed_T1)

    # use classifiers tensor.upfold to crop the patch.
    patches_tensor = image_tensor.unfold(1, patch_size, stride_size).unfold(2, patch_size, stride_size).unfold(3, patch_size, stride_size).contiguous()
    # the dimension of patch_tensor should be [1, patch_num1, patch_num2, patch_num3, patch_size1, patch_size2, patch_size3]
    patches_tensor = patches_tensor.view(-1, patch_size, patch_size, patch_size)

    output_patch = []
    for index_patch in range(patches_tensor.shape[0]):
        extracted_patch = patches_tensor[index_patch, ...].unsqueeze_(0)  # add one dimension
        # save into .pt format
        output_patch.append(
                os.path.join(
                    basedir,
                    os.path.basename(preprocessed_T1).split('.pt')[0]
                    + '_patchsize-'
                    + str(patch_size)
                    + '_stride-'
                    + str(stride_size)
                    + '_patch-'
                    + str(index_patch)
                    + '.pt'
                    )
                )
        torch.save(extracted_patch.clone(), output_patch[index_patch])

    return output_patch


def save_as_pt(input_img):
    """
    This function transforms  nii.gz file into .pt format, in order to train
    the classifiers model more efficient when loading the data.
    :param input_img:
    :return:
    """

    import torch
    import os
    import nibabel as nib

    basedir = os.getcwd()
    image_array = nib.load(input_img).get_fdata()
    image_tensor = torch.from_numpy(image_array).unsqueeze(0).float()
    # make sure the tensor dtype is torch.float32
    output_file = os.path.join(basedir, os.path.basename(input_img).split('.nii.gz')[0] + '.pt')
    # save
    torch.save(image_tensor.clone(), output_file)

    return output_file

# Get containers to produce the CAPS structure


def container_from_filename(bids_or_caps_filename):
    """Extract container from BIDS or CAPS file.
    Args:
       bids_or_caps_filename (str): full path to BIDS or CAPS filename.
    Returns:
       Container path of the form "subjects/<participant_id>/<session_id>"
    Examples:
       >>> from clinica.utils.nipype import container_from_filename
       >>> container_from_filename('/path/to/bids/sub-CLNC01/ses-M00/anat/sub-CLNC01_ses-M00_T1w.nii.gz')
               'subjects/sub-CLNC01/ses-M00'
       >>> container_from_filename('caps/subjects/sub-CLNC01/ses-M00/dwi/preprocessing/sub-CLNC01_ses-M00_preproc.nii')
               'subjects/sub-CLNC01/ses-M00'
    """

    from os.path import join
    import re
    m = re.search(r'(sub-[a-zA-Z0-9]+)/(ses-[a-zA-Z0-9]+)', bids_or_caps_filename)
    if m is None:
        raise ValueError('Input filename is not in a BIDS or CAPS compliant format.'
                         'It does not contain the participant and session ID.')
    subject = m.group(1)
    session = m.group(2)
    return join('subjects', subject, session)


def get_data_datasink(image_id):
    return image_id
